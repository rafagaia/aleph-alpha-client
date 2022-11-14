import os
import pytest
from aleph_alpha_client.aleph_alpha_client import AsyncClient
from aleph_alpha_client.completion import CompletionRequest
from aleph_alpha_client.prompt import Prompt
from aleph_alpha_client.detokenization import DetokenizationRequest
from aleph_alpha_client.tokenization import TokenizationRequest
from aleph_alpha_client.embedding import (
    EmbeddingRequest,
    SemanticEmbeddingRequest,
    SemanticRepresentation,
)
from aleph_alpha_client.summarization import SummarizationRequest
from aleph_alpha_client.evaluation import EvaluationRequest
from aleph_alpha_client.qa import QaRequest
from aleph_alpha_client.explanation import ExplanationRequest
from aleph_alpha_client.document import Document
from .common import (
    async_client,
    model_name,
    checkpoint_name,
    qa_checkpoint_name,
    summarization_checkpoint_name,
)


@pytest.mark.needs_api
async def test_can_use_async_client_without_context_manager(model_name: str):
    request = CompletionRequest(
        prompt=Prompt.from_text(""),
        maximum_tokens=7,
    )
    token = os.environ["TEST_TOKEN"]
    client = AsyncClient(token, host=os.environ["TEST_API_URL"])
    try:
        _ = await client.complete(request, model=model_name)
    finally:
        await client.close()


@pytest.mark.needs_api
async def test_can_complete_with_async_client(async_client: AsyncClient, model_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = CompletionRequest(
        prompt=Prompt.from_text(""),
        maximum_tokens=7,
    )

    response = await async_client.complete(request, model=model_name)
    assert len(response.completions) == 1
    assert response.model_version is not None


@pytest.mark.needs_api
async def test_can_complete_with_async_client_against_checkpoint(async_client: AsyncClient, checkpoint_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = CompletionRequest(
        prompt=Prompt.from_text(""),
        maximum_tokens=7,
    )
    
    response = await async_client.complete(request, checkpoint=checkpoint_name)
    assert len(response.completions) == 1
    assert response.model_version is not None


@pytest.mark.needs_api
async def test_can_detokenization_with_async_client(async_client: AsyncClient, model_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = DetokenizationRequest(token_ids=[2, 3, 4])
    
    response = await async_client.detokenize(request, model=model_name)
    assert len(response.result) > 0


@pytest.mark.needs_api
async def test_can_detokenization_with_async_client_with_checkpoint(async_client: AsyncClient, checkpoint_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = DetokenizationRequest(token_ids=[2, 3, 4])
    
    response = await async_client.detokenize(request, checkpoint=checkpoint_name)
    assert len(response.result) > 0


@pytest.mark.needs_api
async def test_can_tokenize_with_async_client(async_client: AsyncClient, model_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = TokenizationRequest(prompt="hello", token_ids=True, tokens=True)
    
    response = await async_client.tokenize(request, model=model_name)
    assert response.tokens and len(response.tokens) == 1
    assert response.token_ids and len(response.token_ids) == 1


@pytest.mark.needs_api
async def test_can_tokenize_with_async_client_with_checkpoint(async_client: AsyncClient, checkpoint_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = TokenizationRequest(prompt="hello", token_ids=True, tokens=True)
    
    response = await async_client.tokenize(request, checkpoint=checkpoint_name)
    assert response.tokens and len(response.tokens) == 1
    assert response.token_ids and len(response.token_ids) == 1


@pytest.mark.needs_api
async def test_can_embed_with_async_client(async_client: AsyncClient, model_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = request = EmbeddingRequest(
        prompt=Prompt.from_text("abc"), layers=[-1], pooling=["mean"], tokens=True
    )
    
    response = await async_client.embed(request, model=model_name)
    assert response.model_version is not None
    assert response.embeddings and len(response.embeddings) == len(
        request.pooling
    ) * len(request.layers)
    assert response.tokens is not None


@pytest.mark.needs_api
async def test_can_embed_with_async_client_against_checkpoint(async_client: AsyncClient, checkpoint_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = request = EmbeddingRequest(
        prompt=Prompt.from_text("abc"), layers=[-1], pooling=["mean"], tokens=True
    )
    
    response = await async_client.embed(request, checkpoint=checkpoint_name)
    assert response.model_version is not None
    assert response.embeddings and len(response.embeddings) == len(
        request.pooling
    ) * len(request.layers)
    assert response.tokens is not None


@pytest.mark.needs_api
async def test_can_semantic_embed_with_async_client(async_client: AsyncClient, model_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = SemanticEmbeddingRequest(
        prompt=Prompt.from_text("hello"),
        representation=SemanticRepresentation.Symmetric,
        compress_to_size=128,
    )
    
    response = await async_client.semantic_embed(request, model=model_name)
    assert response.model_version is not None
    assert response.embedding
    assert len(response.embedding) == 128


@pytest.mark.needs_api
async def test_can_semantic_embed_with_async_client_against_checkpoint(async_client: AsyncClient, checkpoint_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = SemanticEmbeddingRequest(
        prompt=Prompt.from_text("hello"),
        representation=SemanticRepresentation.Symmetric,
        compress_to_size=128,
    )
    
    response = await async_client.semantic_embed(request, checkpoint=checkpoint_name)
    assert response.model_version is not None
    assert response.embedding
    assert len(response.embedding) == 128


@pytest.mark.needs_api
async def test_can_evaluate_with_async_client(async_client: AsyncClient, model_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = EvaluationRequest(
        prompt=Prompt.from_text("hello"), completion_expected="world"
    )
    
    response = await async_client.evaluate(request, model=model_name)
    assert response.model_version is not None
    assert response.result is not None


@pytest.mark.needs_api
async def test_can_evaluate_with_async_client_against_checkpoint(async_client: AsyncClient, checkpoint_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = EvaluationRequest(
        prompt=Prompt.from_text("hello"), completion_expected="world"
    )
    
    response = await async_client.evaluate(request, checkpoint=checkpoint_name)
    assert response.model_version is not None
    assert response.result is not None


@pytest.mark.needs_api
async def test_can_qa_with_async_client(async_client: AsyncClient):
    token = os.environ.get("TEST_TOKEN")
    request = QaRequest(
        query="Who likes pizza?",
        documents=[Document.from_text("Andreas likes pizza.")],
    )
    
    response = await async_client.qa(request, model="luminous-extended")
    assert len(response.answers) == 1
    assert response.model_version is not None
    assert response.answers[0].score > 0.0


@pytest.mark.needs_api
async def test_can_qa_with_async_client_against_checkpoint(async_client: AsyncClient, qa_checkpoint_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = QaRequest(
        query="Who likes pizza?",
        documents=[Document.from_text("Andreas likes pizza.")],
    )
    
    response = await async_client.qa(request, checkpoint=qa_checkpoint_name)
    assert len(response.answers) == 1
    assert response.model_version is not None
    assert response.answers[0].score > 0.5


@pytest.mark.needs_api
async def test_can_summarize_with_async_client(async_client: AsyncClient):
    token = os.environ.get("TEST_TOKEN")
    request = SummarizationRequest(
        document=Document.from_text("Andreas likes pizza."),
    )
    
    response = await async_client.summarize(request, model="luminous-extended")
    assert response.summary is not None
    assert response.model_version is not None


@pytest.mark.needs_api
async def test_can_summarize_with_async_client_against_checkpoint(
    async_client: AsyncClient, summarization_checkpoint_name: str,
):
    token = os.environ.get("TEST_TOKEN")
    request = SummarizationRequest(
        document=Document.from_text("Andreas likes pizza."),
    )
    
    response = await async_client.summarize(
        request, checkpoint=summarization_checkpoint_name
    )
    assert response.summary is not None
    assert response.model_version is not None

@pytest.mark.needs_api
async def test_can_explain_with_async_client(async_client: AsyncClient, model_name: str):
    token = os.environ.get("TEST_TOKEN")
    request = ExplanationRequest(
        prompt=Prompt.from_text("An apple a day"),
        target=" keeps the doctor away",
        suppression_factor=0.1,
    )
    
    response = await async_client._explain(request, model=model_name)
    assert response.result


@pytest.mark.needs_api
async def test_can_explain_with_async_client_against_checkpoint(
    async_client: AsyncClient, checkpoint_name: str,
):
    token = os.environ.get("TEST_TOKEN")
    request = ExplanationRequest(
        prompt=Prompt.from_text("An apple a day"),
        target=" keeps the doctor away",
        suppression_factor=0.1,
    )
    
    response = await async_client._explain(
        request, checkpoint=checkpoint_name
    )
    assert response.result
    