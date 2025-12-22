import { IndexFlatIP } from 'faiss-node';

export interface Document {
  id: string;
  content: string;
  metadata: Record<string, string>;
  score?: number;
}

export class VectorStore {
  private index: IndexFlatIP;
  private documents: Map<string, Document> = new Map();
  private embeddings: Map<string, number[]> = new Map();

  constructor() {
    this.index = new IndexFlatIP(1536); // OpenAI embedding dimension
  }

  async addDocument(document: Document): Promise<void> {
    // Generate embedding for the document content
    const embedding = await this.generateEmbedding(document.content);

    // Store document and embedding
    this.documents.set(document.id, document);
    this.embeddings.set(document.id, embedding);

    // Add to FAISS index
    this.index.add(embedding);
  }

  async search(query: string, topK: number, threshold: number): Promise<Document[]> {
    if (this.documents.size === 0) {
      return [];
    }

    // Generate embedding for query
    const queryEmbedding = await this.generateEmbedding(query);

    // Search in FAISS index
    const results = this.index.search(queryEmbedding, topK);

    // Convert results to documents with scores
    const documents: Document[] = [];
    const documentIds = Array.from(this.documents.keys());

    for (let i = 0; i < results.labels.length; i++) {
      const score = results.distances[i];
      if (score >= threshold) {
        const docId = documentIds[results.labels[i]];
        const doc = this.documents.get(docId);
        if (doc) {
          documents.push({
            ...doc,
            score,
          });
        }
      }
    }

    return documents;
  }

  async deleteDocument(documentId: string): Promise<void> {
    this.documents.delete(documentId);
    this.embeddings.delete(documentId);
    // Note: FAISS doesn't support deletion, would need to rebuild index
    // For production, consider using a database-backed vector store
  }

  private async generateEmbedding(text: string): Promise<number[]> {
    // Placeholder for embedding generation
    // In production, use OpenAI API or other embedding service
    return new Array(1536).fill(0).map(() => Math.random());
  }
}
