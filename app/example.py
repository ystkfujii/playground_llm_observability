from langfuse.decorators import observe, langfuse_context
from langfuse.openai import openai # OpenAI integration
from langfuse.api import AnnotationQueueObjectType, CreateAnnotationQueueItemRequest, AnnotationQueueStatus
from langfuse import Langfuse

langfuse = Langfuse()

@observe()
def story():
    langfuse.api.annotation_queues.create_queue_item(
        queue_id="cm9a1dv7k0bt4ad07wq1ko2nn",
        request=CreateAnnotationQueueItemRequest(
            object_id=langfuse_context.get_current_observation_id(),
            object_type=AnnotationQueueObjectType.OBSERVATION,
            status=AnnotationQueueStatus.PENDING,
        ),
    )
    langfuse_context.score_current_trace(
        name="score 3",
        value="a",
        data_type="CATEGORICAL",
    )

    return openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {"role": "system", "content": "あなたは有能なアシスタントです。"},
          {"role": "user", "content": "世界について1文で教えてください"},
        ],
    ).choices[0].message.content

@observe()
def main():
    return story()

print(main())
