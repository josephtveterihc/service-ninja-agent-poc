import OpenAI from 'openai';
import { Document } from './vector-store';

export class AIService {
  private openai: OpenAI;

  constructor(apiKey: string) {
    this.openai = new OpenAI({
      apiKey,
    });
  }

  async generateAnswer(query: string, documents: Document[]): Promise<string> {
    if (documents.length === 0) {
      return 'I could not find relevant information to answer your question.';
    }

    const context = documents.map((doc, index) => `Source ${index + 1}: ${doc.content}`).join('\n\n');

    const prompt = this.buildPrompt(query, context);

    try {
      const response = await this.openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content:
              'You are a helpful assistant that answers questions based on provided context. Only use information from the provided sources.',
          },
          {
            role: 'user',
            content: prompt,
          },
        ],
        max_tokens: 500,
        temperature: 0.7,
      });

      return response.choices[0]?.message?.content || 'Unable to generate answer.';
    } catch (error) {
      console.error('OpenAI API error:', error);
      return 'Error generating answer. Please try again.';
    }
  }

  private buildPrompt(query: string, context: string): string {
    return `
Context:
${context}

Question: ${query}

Please provide a comprehensive answer based on the context provided above. If the context doesn't contain enough information to answer the question, please say so.
    `.trim();
  }
}
