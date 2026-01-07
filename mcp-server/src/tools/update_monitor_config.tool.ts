import type { JsonObj, McpToolCallResult } from '../types'

interface UpdateMonitorConfigArgs {
  monitorId: string
  config: {
    checkInterval?: number
    timeout?: number
    alertContacts?: string[]
    enabled?: boolean
    thresholds?: {
      responseTime?: number
      errorRate?: number
      uptime?: number
    }
  }
}

export function updateMonitorConfigTool(args: JsonObj): McpToolCallResult {
  try {
    const { monitorId, config } = args as UpdateMonitorConfigArgs

    // Input validation
    if (!monitorId || typeof monitorId !== 'string' || monitorId.trim().length === 0) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'monitorId is required and must be a non-empty string',
          },
        ],
      }
    }

    if (!config || typeof config !== 'object') {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'config is required and must be an object',
          },
        ],
      }
    }

    // Validate and sanitize config values
    const validatedConfig: {
      checkInterval?: number
      timeout?: number
      alertContacts?: string[]
      enabled?: boolean
      thresholds?: {
        responseTime?: number
        errorRate?: number
        uptime?: number
      }
    } = {}

    if (config.checkInterval !== undefined) {
      if (typeof config.checkInterval === 'number' && config.checkInterval >= 30 && config.checkInterval <= 3600) {
        validatedConfig.checkInterval = config.checkInterval
      } else {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: 'checkInterval must be a number between 30 and 3600 seconds',
            },
          ],
        }
      }
    }

    if (config.timeout !== undefined) {
      if (typeof config.timeout === 'number' && config.timeout >= 5 && config.timeout <= 120) {
        validatedConfig.timeout = config.timeout
      } else {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: 'timeout must be a number between 5 and 120 seconds',
            },
          ],
        }
      }
    }

    if (config.alertContacts !== undefined) {
      if (Array.isArray(config.alertContacts)) {
        validatedConfig.alertContacts = config.alertContacts.filter((contact) => typeof contact === 'string' && contact.includes('@') && contact.length > 3)
      } else {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: 'alertContacts must be an array of email addresses',
            },
          ],
        }
      }
    }

    if (config.enabled !== undefined) {
      if (typeof config.enabled === 'boolean') {
        validatedConfig.enabled = config.enabled
      } else {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: 'enabled must be a boolean value',
            },
          ],
        }
      }
    }

    if (config.thresholds !== undefined) {
      if (typeof config.thresholds === 'object') {
        const thresholds: {
          responseTime?: number
          errorRate?: number
          uptime?: number
        } = {}

        if (config.thresholds.responseTime !== undefined) {
          if (typeof config.thresholds.responseTime === 'number' && config.thresholds.responseTime > 0) {
            thresholds.responseTime = config.thresholds.responseTime
          } else {
            return {
              isError: true,
              content: [
                {
                  type: 'text',
                  text: 'responseTime threshold must be a positive number (milliseconds)',
                },
              ],
            }
          }
        }

        if (config.thresholds.errorRate !== undefined) {
          if (typeof config.thresholds.errorRate === 'number' && config.thresholds.errorRate >= 0 && config.thresholds.errorRate <= 1) {
            thresholds.errorRate = config.thresholds.errorRate
          } else {
            return {
              isError: true,
              content: [
                {
                  type: 'text',
                  text: 'errorRate threshold must be a number between 0 and 1',
                },
              ],
            }
          }
        }

        if (config.thresholds.uptime !== undefined) {
          if (typeof config.thresholds.uptime === 'number' && config.thresholds.uptime >= 0 && config.thresholds.uptime <= 1) {
            thresholds.uptime = config.thresholds.uptime
          } else {
            return {
              isError: true,
              content: [
                {
                  type: 'text',
                  text: 'uptime threshold must be a number between 0 and 1',
                },
              ],
            }
          }
        }

        if (Object.keys(thresholds).length > 0) {
          validatedConfig.thresholds = thresholds
        }
      } else {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: 'thresholds must be an object',
            },
          ],
        }
      }
    }

    const result = {
      success: true,
      monitorId: monitorId.trim(),
      updatedConfig: validatedConfig,
      updatedAt: new Date().toISOString(),
      previousConfig: {
        // Mock previous config for comparison
        checkInterval: 300,
        timeout: 10,
        alertContacts: ['admin@example.com'],
        enabled: true,
        thresholds: {
          responseTime: 1000,
          errorRate: 0.05,
          uptime: 0.99,
        },
      },
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
      _meta: {
        toolName: 'update_monitor_config',
        executionTime: Date.now(),
      },
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to update monitor config: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}
