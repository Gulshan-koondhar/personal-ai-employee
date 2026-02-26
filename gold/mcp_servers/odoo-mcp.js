// odoo-mcp.js - Odoo MCP Server for AI Employee
// This server provides Odoo/Accounting integration capabilities to Claude Code

const { createServer } = require('http');
const { parse } = require('url');
const axios = require('axios').default;

// MCP capabilities definition
const capabilities = {
  resources: [],
  tools: [
    {
      name: "create_invoice",
      description: "Create an invoice in Odoo",
      inputSchema: {
        type: "object",
        properties: {
          partner_id: { type: "integer", description: "Customer ID in Odoo" },
          invoice_lines: {
            type: "array",
            items: {
              type: "object",
              properties: {
                product_id: { type: "integer", description: "Product ID" },
                quantity: { type: "number", description: "Quantity" },
                price_unit: { type: "number", description: "Unit price" }
              },
              required: ["product_id", "quantity", "price_unit"]
            }
          },
          journal_id: { type: "integer", description: "Journal ID (optional, defaults to sales)" }
        },
        required: ["partner_id", "invoice_lines"]
      }
    },
    {
      name: "search_invoices",
      description: "Search for invoices in Odoo",
      inputSchema: {
        type: "object",
        properties: {
          domain: {
            type: "array",
            description: "Search domain (e.g., [['state', '=', 'posted']])",
            items: { type: "array" }
          }
        }
      }
    },
    {
      name: "get_invoice_details",
      description: "Get detailed information about a specific invoice",
      inputSchema: {
        type: "object",
        properties: {
          invoice_id: { type: "integer", description: "Invoice ID" }
        },
        required: ["invoice_id"]
      }
    },
    {
      name: "create_expense",
      description: "Create an expense record in Odoo",
      inputSchema: {
        type: "object",
        properties: {
          employee_id: { type: "integer", description: "Employee ID" },
          product_id: { type: "integer", description: "Product/Expense category ID" },
          description: { type: "string", description: "Expense description" },
          total_amount: { type: "number", description: "Total expense amount" },
          date: { type: "string", description: "Expense date (YYYY-MM-DD)" }
        },
        required: ["employee_id", "product_id", "description", "total_amount"]
      }
    },
    {
      name: "get_financial_summary",
      description: "Get financial summary for a period",
      inputSchema: {
        type: "object",
        properties: {
          start_date: { type: "string", description: "Start date (YYYY-MM-DD)" },
          end_date: { type: "string", description: "End date (YYYY-MM-DD)" }
        }
      }
    },
    {
      name: "create_contact",
      description: "Create a new contact in Odoo",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Contact name" },
          email: { type: "string", description: "Contact email" },
          phone: { type: "string", description: "Contact phone" },
          is_customer: { type: "boolean", description: "Whether contact is a customer (default: true)" },
          is_supplier: { type: "boolean", description: "Whether contact is a supplier (default: false)" }
        },
        required: ["name"]
      }
    }
  ]
};

// Simple in-memory storage for demonstration (in real implementation, this would connect to Odoo)
let mockInvoices = [];
let mockExpenses = [];
let mockContacts = [];
let invoiceIdCounter = 1000;
let contactIdCounter = 2000;

// Mock functions to simulate Odoo API calls
async function createInvoice({ partner_id, invoice_lines, journal_id }) {
  const invoiceId = invoiceIdCounter++;
  const total = invoice_lines.reduce((sum, line) => sum + (line.quantity * line.price_unit), 0);

  const newInvoice = {
    id: invoiceId,
    partner_id,
    invoice_lines,
    journal_id: journal_id || 1, // Default sales journal
    total,
    state: 'draft',
    create_date: new Date().toISOString(),
    number: `INV${String(invoiceId).padStart(5, '0')}`
  };

  mockInvoices.push(newInvoice);

  console.log(`[ODOO MCP] Created invoice ${newInvoice.number} for partner ${partner_id}`);
  return {
    success: true,
    invoice_id: invoiceId,
    invoice_number: newInvoice.number,
    message: `Invoice ${newInvoice.number} created successfully (simulated)`
  };
}

async function searchInvoices({ domain = [] }) {
  console.log(`[ODOO MCP] Searching invoices with domain:`, domain);

  // In real implementation, this would call Odoo's searchRead API
  // For demo, return all invoices with optional filtering
  let results = [...mockInvoices];

  // Apply simple filtering based on domain (simulated)
  if (domain && domain.length > 0) {
    // This is a simplified simulation - real implementation would use Odoo's search capabilities
    if (domain.some(condition => condition[0] === 'state' && condition[1] === '=' && condition[2] === 'posted')) {
      results = results.filter(inv => inv.state === 'posted');
    }
  }

  return {
    success: true,
    invoices: results,
    count: results.length
  };
}

async function getInvoiceDetails({ invoice_id }) {
  console.log(`[ODOO MCP] Getting details for invoice ID: ${invoice_id}`);

  const invoice = mockInvoices.find(inv => inv.id === invoice_id);
  if (!invoice) {
    throw new Error(`Invoice with ID ${invoice_id} not found`);
  }

  return {
    success: true,
    invoice: invoice
  };
}

async function createExpense({ employee_id, product_id, description, total_amount, date }) {
  const expenseId = invoiceIdCounter++; // Reuse counter for demo

  const newExpense = {
    id: expenseId,
    employee_id,
    product_id,
    description,
    total_amount,
    date: date || new Date().toISOString().split('T')[0],
    state: 'draft'
  };

  mockExpenses.push(newExpense);

  console.log(`[ODOO MCP] Created expense for employee ${employee_id}, amount: ${total_amount}`);
  return {
    success: true,
    expense_id: expenseId,
    message: `Expense record created successfully (simulated)`
  };
}

async function getFinancialSummary({ start_date, end_date }) {
  console.log(`[ODOO MCP] Getting financial summary from ${start_date} to ${end_date}`);

  // Calculate totals based on mock data
  const totalInvoiced = mockInvoices
    .filter(inv => inv.state === 'posted')
    .reduce((sum, inv) => sum + inv.total, 0);

  const totalExpenses = mockExpenses.reduce((sum, exp) => sum + exp.total_amount, 0);

  const profit = totalInvoiced - totalExpenses;

  return {
    success: true,
    summary: {
      period: { start_date, end_date },
      total_invoiced: totalInvoiced,
      total_expenses: totalExpenses,
      profit: profit,
      invoice_count: mockInvoices.filter(inv => inv.state === 'posted').length,
      expense_count: mockExpenses.length
    }
  };
}

async function createContact({ name, email, phone, is_customer = true, is_supplier = false }) {
  const contactId = contactIdCounter++;

  const newContact = {
    id: contactId,
    name,
    email,
    phone,
    is_customer,
    is_supplier,
    create_date: new Date().toISOString()
  };

  mockContacts.push(newContact);

  console.log(`[ODOO MCP] Created contact: ${name} (ID: ${contactId})`);
  return {
    success: true,
    contact_id: contactId,
    message: `Contact ${name} created successfully (simulated)`
  };
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

    req.on('end', async () => {
      try {
        const { toolName, parameters } = JSON.parse(body);

        let result;
        switch (toolName) {
          case 'create_invoice':
            result = await createInvoice(parameters);
            break;
          case 'search_invoices':
            result = await searchInvoices(parameters);
            break;
          case 'get_invoice_details':
            result = await getInvoiceDetails(parameters);
            break;
          case 'create_expense':
            result = await createExpense(parameters);
            break;
          case 'get_financial_summary':
            result = await getFinancialSummary(parameters);
            break;
          case 'create_contact':
            result = await createContact(parameters);
            break;
          default:
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: `Unknown tool: ${toolName}` }));
            return;
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
      } catch (error) {
        console.error('[ODOO MCP] Error processing request:', error);
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

const PORT = process.env.PORT || 8081; // Use different port than email MCP
const HOST = process.env.HOST || '127.0.0.1';

server.listen(PORT, HOST, () => {
  console.log(`[ODOO MCP] Server running at http://${HOST}:${PORT}/`);
  console.log('[ODOO MCP] Available tools:', capabilities.tools.map(t => t.name).join(', '));
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n[ODOO MCP] Shutting down server...');
  server.close(() => {
    console.log('[ODOO MCP] Server closed');
    process.exit(0);
  });
});