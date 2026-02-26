// email-mcp.js - Email MCP Server for AI Employee
// This server provides email capabilities to Claude Code

const { createServer } = require('http');
const { parse } = require('url');
const { Readable } = require('stream');

// Simple in-memory storage for demonstration
let emailQueue = [];

// MCP capabilities definition
const capabilities = {
  resources: [],
  tools: [
    {
      name: "send_email",
      description: "Send an email to a recipient",
      inputSchema: {
        type: "object",
        properties: {
          to: { type: "string", description: "Recipient email address" },
          subject: { type: "string", description: "Email subject" },
          body: { type: "string", description: "Email body content" },
          cc: { type: "string", description: "CC recipients (optional)" },
          bcc: { type: "string", description: "BCC recipients (optional)" }
        },
        required: ["to", "subject", "body"]
      }
    },
    {
      name: "queue_email",
      description: "Queue an email for later sending (requires approval)",
      inputSchema: {
        type: "object",
        properties: {
          to: { type: "string", description: "Recipient email address" },
          subject: { type: "string", description: "Email subject" },
          body: { type: "string", description: "Email body content" },
          priority: { type: "string", description: "Priority: low, medium, high" }
        },
        required: ["to", "subject", "body"]
      }
    },
    {
      name: "get_queued_emails",
      description: "Get list of queued emails awaiting approval",
      inputSchema: {
        type: "object",
        properties: {}
      }
    },
    {
      name: "get_sent_emails",
      description: "Get list of recently sent emails",
      inputSchema: {
        type: "object",
        properties: {}
      }
    }
  ]
};

// Simple email sending function (simulated)
function sendEmail({ to, subject, body, cc, bcc }) {
  const email = {
    id: Date.now().toString(),
    to,
    subject,
    body,
    cc,
    bcc,
    timestamp: new Date().toISOString(),
    status: 'sent'
  };

  console.log(`[EMAIL MCP] Sending email to: ${to}, subject: ${subject}`);
  // In a real implementation, this would actually send the email via SMTP or API
  return { success: true, emailId: email.id, message: 'Email sent successfully (simulated)' };
}

// Queue email for approval
function queueEmail({ to, subject, body, priority = 'medium' }) {
  const email = {
    id: Date.now().toString(),
    to,
    subject,
    body,
    priority,
    timestamp: new Date().toISOString(),
    status: 'queued'
  };

  emailQueue.push(email);
  console.log(`[EMAIL MCP] Queued email for approval: ${to}, subject: ${subject}`);
  return { success: true, emailId: email.id, message: 'Email queued for approval' };
}

// Get queued emails
function getQueuedEmails() {
  console.log(`[EMAIL MCP] Returning ${emailQueue.length} queued emails`);
  return { queued_emails: emailQueue };
}

// Get sent emails (simulated)
function getSentEmails() {
  const sentEmails = [
    { id: 'sent1', to: 'test@example.com', subject: 'Sample Sent Email', timestamp: new Date().toISOString() }
  ];
  console.log(`[EMAIL MCP] Returning ${sentEmails.length} sent emails`);
  return { sent_emails: sentEmails };
}

// Handle incoming MCP requests
function handleRequest(req, res) {
  const parsedUrl = parse(req.url, true);
  const path = parsedUrl.pathname;

  // MCP protocol endpoints
  if (path === '/capabilities.json') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(capabilities, null, 2));
  }
  else if (req.method === 'POST' && path === '/execute-tool') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });

    req.on('end', () => {
      try {
        const { toolName, parameters } = JSON.parse(body);

        let result;
        switch (toolName) {
          case 'send_email':
            result = sendEmail(parameters);
            break;
          case 'queue_email':
            result = queueEmail(parameters);
            break;
          case 'get_queued_emails':
            result = getQueuedEmails();
            break;
          case 'get_sent_emails':
            result = getSentEmails();
            break;
          default:
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: `Unknown tool: ${toolName}` }));
            return;
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
      } catch (error) {
        console.error('[EMAIL MCP] Error processing request:', error);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: error.message }));
      }
    });
  }
  else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
  }
}

// Create and start server
const server = createServer(handleRequest);

const PORT = process.env.PORT || 8080;
const HOST = process.env.HOST || '127.0.0.1';

server.listen(PORT, HOST, () => {
  console.log(`[EMAIL MCP] Server running at http://${HOST}:${PORT}/`);
  console.log('[EMAIL MCP] Available tools:', capabilities.tools.map(t => t.name).join(', '));
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n[EMAIL MCP] Shutting down server...');
  server.close(() => {
    console.log('[EMAIL MCP] Server closed');
    process.exit(0);
  });
});