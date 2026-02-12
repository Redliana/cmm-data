"""Upload batch input to GCS and submit a Vertex AI batch inference job.

Usage:
    python submit_batch.py                    # upload + submit
    python submit_batch.py --monitor          # upload + submit + poll until done
    python submit_batch.py --status JOB_NAME  # check status of existing job
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from config import (
    GCP_PROJECT,
    GCP_REGION,
    GCS_BUCKET,
    GCS_INPUT_PREFIX,
    GCS_OUTPUT_PREFIX,
    GEMINI_MODEL,
    OUTPUT_DIR,
)


def upload_to_gcs(local_path: Path, gcs_prefix: str) -> str:
    """Upload a local file to GCS and return the gs:// URI."""
    from google.cloud import storage

    client = storage.Client(project=GCP_PROJECT)
    bucket = client.bucket(GCS_BUCKET)
    blob_name = f"{gcs_prefix}/{local_path.name}"
    blob = bucket.blob(blob_name)

    print(f"Uploading {local_path.name} to gs://{GCS_BUCKET}/{blob_name} ...")
    blob.upload_from_filename(str(local_path))
    gcs_uri = f"gs://{GCS_BUCKET}/{blob_name}"
    print(f"Upload complete: {gcs_uri}")
    return gcs_uri


def submit_batch_job(input_uri: str, monitor: bool = False) -> dict:
    """Submit a Vertex AI batch prediction job via google-genai SDK."""
    from google import genai

    client = genai.Client(
        vertexai=True,
        project=GCP_PROJECT,
        location=GCP_REGION,
    )

    output_uri = f"gs://{GCS_BUCKET}/{GCS_OUTPUT_PREFIX}"

    print("Submitting batch job...")
    print(f"  Model: {GEMINI_MODEL}")
    print(f"  Input: {input_uri}")
    print(f"  Output: {output_uri}")

    batch_job = client.batches.create(
        model=GEMINI_MODEL,
        src=input_uri,
        config=genai.types.CreateBatchJobConfig(
            dest=output_uri,
            display_name=f"cmm-paper-analysis-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        ),
    )

    job_name = batch_job.name
    print(f"\nJob submitted: {job_name}")
    print(f"State: {batch_job.state}")

    # Save metadata
    metadata = {
        "job_name": job_name,
        "model": GEMINI_MODEL,
        "input_uri": input_uri,
        "output_uri": output_uri,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "state": str(batch_job.state),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = OUTPUT_DIR / "job_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Job metadata saved to {meta_path}")

    if monitor:
        poll_job(client, job_name)

    return metadata


def poll_job(client=None, job_name: str | None = None) -> None:
    """Poll a batch job until completion."""
    if client is None:
        from google import genai

        client = genai.Client(
            vertexai=True,
            project=GCP_PROJECT,
            location=GCP_REGION,
        )

    if job_name is None:
        meta_path = OUTPUT_DIR / "job_metadata.json"
        if not meta_path.exists():
            print("No job_metadata.json found. Provide --status JOB_NAME.")
            return
        metadata = json.loads(meta_path.read_text())
        job_name = metadata["job_name"]

    print(f"\nMonitoring job: {job_name}")
    terminal_states = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"}

    while True:
        batch_job = client.batches.get(name=job_name)
        state = str(batch_job.state)
        now = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(f"  [{now}] State: {state}")

        if state in terminal_states or "SUCCEEDED" in state or "FAILED" in state:
            break

        time.sleep(60)  # Poll every minute

    print(f"\nJob finished with state: {state}")

    # Update metadata
    meta_path = OUTPUT_DIR / "job_metadata.json"
    if meta_path.exists():
        metadata = json.loads(meta_path.read_text())
        metadata["final_state"] = state
        metadata["completed_at"] = datetime.now(timezone.utc).isoformat()
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit Vertex AI batch inference job")
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Poll until job completes",
    )
    parser.add_argument(
        "--status",
        type=str,
        help="Check status of an existing job by name",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to batch input JSONL (default: output/batch_input.jsonl)",
    )
    args = parser.parse_args()

    if args.status:
        poll_job(job_name=args.status)
        return

    input_path = Path(args.input) if args.input else OUTPUT_DIR / "batch_input.jsonl"
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Run prepare_batch.py first.")
        return

    # Upload to GCS
    gcs_uri = upload_to_gcs(input_path, GCS_INPUT_PREFIX)

    # Submit batch job
    submit_batch_job(gcs_uri, monitor=args.monitor)


if __name__ == "__main__":
    main()
