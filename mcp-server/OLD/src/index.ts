import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { RAGServer } from './grpc/server';
import { VectorStore } from './services/vector-store';
import { AIService } from './services/ai-service';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const GRPC_PORT = process.env.GRPC_PORT || 50051;

app.use(helmet());
app.use(cors());
app.use(express.json());

async function startServer(): Promise<void> {
  try {
    // Initialize services
    const vectorStore = new VectorStore();
    const aiService = new AIService(process.env.OPENAI_API_KEY || '');

    // Start gRPC server
    const grpcServer = new RAGServer(vectorStore, aiService);
    await grpcServer.start(GRPC_PORT as number);

    // Health check endpoint
    app.get('/health', (req, res) => {
      res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
      });
    });

    app.listen(PORT, () => {
      console.log(`HTTP server running on port ${PORT}`);
      console.log(`gRPC server running on port ${GRPC_PORT}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();
