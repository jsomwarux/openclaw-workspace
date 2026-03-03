/**
 * Embedding generation via @xenova/transformers
 * Model: all-MiniLM-L6-v2 (384 dims, ~22MB, downloads on first use to ~/.cache/xenova)
 */

export const MODEL_NAME = "Xenova/all-MiniLM-L6-v2";
let _pipeline: any = null;

async function getPipeline() {
  if (_pipeline) return _pipeline;

  // Dynamically import to avoid startup cost when embeddings aren't needed
  const { pipeline, env } = await import("@xenova/transformers");

  // Use local cache dir
  env.cacheDir = `${process.env.HOME}/.cache/xenova`;

  console.error(`[embed] Loading model ${MODEL_NAME}...`);
  _pipeline = await pipeline("feature-extraction", MODEL_NAME, {
    quantized: true, // Use quantized model for speed (~22MB vs 90MB)
  });
  console.error("[embed] Model ready.");
  return _pipeline;
}

/**
 * Generate an embedding for a text string.
 * Returns Float32Array of 384 dimensions.
 */
export async function embed(text: string): Promise<Float32Array> {
  const pipe = await getPipeline();

  // Truncate to ~512 tokens worth of chars
  const truncated = text.slice(0, 2048);

  const output = await pipe(truncated, {
    pooling: "mean",
    normalize: true,
  });

  return output.data as Float32Array;
}

/**
 * Embed multiple texts in batch (more efficient).
 */
export async function embedBatch(
  texts: string[],
  onProgress?: (i: number, total: number) => void
): Promise<Float32Array[]> {
  const results: Float32Array[] = [];
  for (let i = 0; i < texts.length; i++) {
    results.push(await embed(texts[i]));
    onProgress?.(i + 1, texts.length);
  }
  return results;
}

/**
 * Cosine similarity between two normalized vectors.
 * Assumes both vectors are L2-normalized (which we do above).
 */
export function cosineSimilarity(a: Float32Array, b: Float32Array): number {
  if (a.length !== b.length) return 0;
  let dot = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
  }
  return dot; // Already normalized → dot product == cosine similarity
}
