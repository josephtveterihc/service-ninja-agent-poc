import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import path from 'path';
import { VectorStore } from '../services/vector-store';
import { AIService } from '../services/ai-service';

const PROTO_PATH = path.join(__dirname, '../../proto/rag.proto');

export class RAGServer {
  private server: grpc.Server;

  constructor(
    private vectorStore: VectorStore,
    private aiService: AIService
  ) {
    this.server = new grpc.Server();
    this.loadProtoAndSetupRoutes();
  }

  private loadProtoAndSetupRoutes(): void {
    const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
      keepCase: true,
      longs: String,
      enums: String,
      defaults: true,
      oneofs: true,
    });

    const protoDescriptor = grpc.loadPackageDefinition(
      packageDefinition
    ) as any;
    const ragService = protoDescriptor.rag.RAGService;

    this.server.addService(ragService.service, {
      Query: this.handleQuery.bind(this),
      AddDocument: this.handleAddDocument.bind(this),
      DeleteDocument: this.handleDeleteDocument.bind(this),
    });
  }

  private async handleQuery(call: any, callback: any): Promise<void> {
    try {
      const { query, top_k = 5, threshold = 0.7 } = call.request;

      // Retrieve relevant documents
      const documents = await this.vectorStore.search(query, top_k, threshold);

      // Generate answer using AI service
      const answer = await this.aiService.generateAnswer(query, documents);

      callback(null, {
        answer,
        sources: documents,
        confidence: documents.length > 0 ? documents[0].score : 0,
      });
    } catch (error) {
      console.error('Query error:', error);
      callback({
        code: grpc.status.INTERNAL,
        details: 'Internal server error',
      });
    }
  }

  private async handleAddDocument(call: any, callback: any): Promise<void> {
    try {
      const { document } = call.request;
      await this.vectorStore.addDocument(document);

      callback(null, {
        success: true,
        message: 'Document added successfully',
      });
    } catch (error) {
      console.error('Add document error:', error);
      callback(null, {
        success: false,
        message: 'Failed to add document',
      });
    }
  }

  private async handleDeleteDocument(call: any, callback: any): Promise<void> {
    try {
      const { document_id } = call.request;
      await this.vectorStore.deleteDocument(document_id);

      callback(null, {
        success: true,
        message: 'Document deleted successfully',
      });
    } catch (error) {
      console.error('Delete document error:', error);
      callback(null, {
        success: false,
        message: 'Failed to delete document',
      });
    }
  }

  async start(port: number): Promise<void> {
    return new Promise((resolve, reject) => {
      this.server.bindAsync(
        `0.0.0.0:${port}`,
        grpc.ServerCredentials.createInsecure(),
        (err) => {
          if (err) {
            reject(err);
          } else {
            this.server.start();
            resolve();
          }
        }
      );
    });
  }
}
