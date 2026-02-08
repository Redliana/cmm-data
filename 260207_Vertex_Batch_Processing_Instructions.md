<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Thank you. How exactly would I conduct the batch processing using Gemini 2.5 deep think? I have a Vertex AI account.

Here's how to conduct batch processing with Gemini 2.5 Deep Think using your Vertex AI account:

## Overview

Vertex AI batch inference provides 50% discounted pricing and processes requests asynchronously with a 24-hour turnaround time. This is ideal for your 1,100 abstract analysis task.[^1]

## Step-by-Step Process

### 1. Prepare Your Input File (JSONL Format)

Create a JSON Lines file where each line contains one request. For scientific abstracts, structure it like this:

```json
{"request": {"contents": [{"parts": [{"text": "Analyze this abstract and determine if it should be included in a gold Q&A dataset about [your topic]. Abstract: [abstract text here]"}]}], "generationConfig": {"temperature": 1.0}}, "custom_id": "abstract_001"}
{"request": {"contents": [{"parts": [{"text": "Analyze this abstract and determine if it should be included in a gold Q&A dataset about [your topic]. Abstract: [abstract text here]"}]}], "generationConfig": {"temperature": 1.0}}, "custom_id": "abstract_002"}
```

Each line must be a complete JSON object with:

- `request`: A valid `GenerateContentRequest` containing your prompt
- `custom_id`: Your unique identifier to track which abstract the response corresponds to[^2]


### 2. Upload Input File to Cloud Storage

Upload your JSONL file to a Google Cloud Storage bucket:

```bash
gsutil cp my-abstracts-batch.jsonl gs://YOUR_BUCKET_NAME/input/
```


### 3. Create the Batch Prediction Job

Using Python with the Vertex AI SDK:

```python
from google.cloud import aiplatform

aiplatform.init(project="YOUR_PROJECT_ID", location="us-central1")

batch_prediction_job = aiplatform.BatchPredictionJob.create(
    job_display_name="abstract-analysis-batch",
    model_name="gemini-2.5-pro-002",  # Use Deep Think model
    gcs_source="gs://YOUR_BUCKET_NAME/input/my-abstracts-batch.jsonl",
    gcs_destination_prefix="gs://YOUR_BUCKET_NAME/output/",
    instances_format="jsonl",
    predictions_format="jsonl"
)
```

Or using the gcloud CLI:

```bash
gcloud ai batch-prediction-jobs create \
  --region=us-central1 \
  --model=gemini-2.5-pro-002 \
  --input-uri=gs://YOUR_BUCKET_NAME/input/my-abstracts-batch.jsonl \
  --output-uri=gs://YOUR_BUCKET_NAME/output/ \
  --display-name=abstract-analysis-batch
```


### 4. Monitor Job Status

Track your batch job progress:

```python
# Get job status
batch_prediction_job.wait_for_completion()

# Or check status
print(batch_prediction_job.state)
```


### 5. Retrieve Results

Once complete (typically within 24 hours), results are written to your output Cloud Storage location as a JSONL file. Each output line contains either a `GenerateContentResponse` or an error status object corresponding to your input requests.[^1][^2]

Download and process results:

```bash
gsutil cp gs://YOUR_BUCKET_NAME/output/*.jsonl ./results/
```


## Important Considerations

**Model specification**: Make sure to use `gemini-2.5-pro-002` or the appropriate Deep Think model identifier. The "thinking" mode may need to be explicitly enabled in your generation config.[^3]

**Rate limits**: Batch processing supports hundreds of thousands of requests in a single job with higher rate limits than real-time API.[^1]

**Combining jobs**: Submit all 1,100 abstracts in one batch job rather than multiple smaller jobs for better throughput.[^1]

**BigQuery alternative**: If you already have abstracts in BigQuery, you can use BigQuery as both input and output source instead of Cloud Storage.[^4]

**Cost savings**: The 50% batch discount applies, but note that if implicit caching is triggered, the 90% cache discount takes precedence (though this is less relevant for your varied abstract analysis task).[^1]

This approach should be highly cost-effective for your one-time analysis of 1,100 scientific abstracts while maintaining the reasoning capabilities of Gemini 2.5 Deep Think.
<span style="display:none">[^10][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-gemini

[^2]: https://ai.google.dev/gemini-api/docs/batch-api

[^3]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking

[^4]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/batch-prediction-api

[^5]: https://cloud.google.com/vertex-ai/generative-ai/pricing

[^6]: https://www.reddit.com/r/LocalLLaMA/comments/1led0lb/google_doubled_the_price_of_gemini_25_flash/

[^7]: https://www.reddit.com/r/LocalLLaMA/comments/1ja0yxn/gemini_batch_api_is_cost_efficient_but/

[^8]: https://www.linkedin.com/posts/ivan-nardini_googlecloud-ai-llm-activity-7353863340848201729-XHOD

[^9]: https://docs.cloud.google.com/vertex-ai/docs/predictions/get-batch-predictions

[^10]: https://github.com/googleapis/python-genai/issues/1590

