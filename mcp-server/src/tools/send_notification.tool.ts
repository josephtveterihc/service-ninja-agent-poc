import { type McpToolCallResponse } from '../types/server.types.js'

interface SendNotificationArgs {
  type: 'email' | 'teams' | 'slack'
  recipient: string
  subject: string
  message: string
  priority?: 'low' | 'normal' | 'high' | 'critical'
  attachments?: string[]
}

export function sendNotificationTool(args: Record<string, any>): McpToolCallResponse {
  try {
    const { 
      type, 
      recipient, 
      subject, 
      message, 
      priority = 'normal',
      attachments = []
    } = args as SendNotificationArgs

    // Input validation
    if (!type || !['email', 'teams', 'slack'].includes(type)) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'type is required and must be one of: email, teams, slack'
        }]
      }
    }

    if (!recipient || typeof recipient !== 'string' || recipient.trim().length === 0) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'recipient is required and must be a non-empty string'
        }]
      }
    }

    if (!subject || typeof subject !== 'string' || subject.trim().length === 0) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'subject is required and must be a non-empty string'
        }]
      }
    }

    if (!message || typeof message !== 'string' || message.trim().length === 0) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'message is required and must be a non-empty string'
        }]
      }
    }

    // Validate recipient format based on type
    if (type === 'email' && !recipient.includes('@')) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'Invalid email format for recipient'
        }]
      }
    }

    if (type === 'teams' && !recipient.startsWith('https://')) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'Teams recipient must be a valid webhook URL'
        }]
      }
    }

    // Validate priority
    const validPriority = ['low', 'normal', 'high', 'critical'].includes(priority) ? priority : 'normal'

    // Validate attachments
    const validAttachments = Array.isArray(attachments) 
      ? attachments.filter(att => typeof att === 'string' && att.length > 0)
      : []

    const notificationId = `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    const result = {
      success: true,
      notificationId,
      type,
      recipient: recipient.trim(),
      subject: subject.trim(),
      message: message.trim(),
      priority: validPriority,
      attachments: validAttachments,
      status: 'sent',
      sentAt: new Date().toISOString()
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }],
      _meta: {
        toolName: 'send_notification',
        executionTime: Date.now()
      }
    }
  } catch (error) {
    return {
      isError: true,
      content: [{
        type: 'text',
        text: `Failed to send notification: ${error instanceof Error ? error.message : 'Unknown error'}`
      }]
    }
  }
}