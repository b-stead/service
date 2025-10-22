-- Main user table
CREATE TABLE "user" (
    "user_id" text NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::text,
    "sub" text NOT NULL, -- Identifier from Firebase,
    "email" text NOT NULL,
    "email_verified" boolean NULL DEFAULT false,
    "first_name" text NOT NULL,
    "last_name" text NOT NULL,
    "birthdate" date NULL,
    "created_date" timestamp NOT NULL DEFAULT now(),
    "updated_at" timestamp NOT NULL DEFAULT now(),
    "is_deleted" boolean NOT NULL DEFAULT false,
    "deleted_at" timestamp NULL
);
-- These indexes express that sub/email must be unique for active (i.e. not deleted) users
CREATE UNIQUE INDEX ON "user" ("sub") WHERE "is_deleted" = FALSE;
CREATE UNIQUE INDEX ON "user" ("email") WHERE "is_deleted" = FALSE;

-- Customers Table
CREATE TABLE "customers" (
    "customer_id" text NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::text,
    "user_id" text NOT NULL REFERENCES "user"("user_id"),
    "name" text,
    "company_name" text,
    "organisation" boolean DEFAULT false,
    "contact_person" text,
    "email" text,
    "phone" text,
    "address_line1" text,
    "address_line2" text,
    "city" text,
    "state" text,
    "postal_code" text,
    "country" text,
    "created_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" boolean NOT NULL DEFAULT false,
    "deleted_at" timestamp NULL
);
CREATE INDEX idx_customers_user_id ON customers ("user_id");

-- Jobs Table
CREATE TABLE "jobs" (
    "job_id" text NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::text,
    "user_id" text NOT NULL REFERENCES "user"("user_id"),
    "customer_id" text NOT NULL REFERENCES "customers"("customer_id") ON DELETE RESTRICT,
    "job_title" text NOT NULL,
    "job_description" text,
    "job_status" text NOT NULL CHECK ("job_status" IN ('pending', 'in_progress', 'completed', 'cancelled')) DEFAULT 'pending',
    "start_date" date,
    "end_date" date,
    "estimated_hours" NUMERIC(8,2),
    "actual_hours" NUMERIC(8,2),
    "daily_rate" NUMERIC(10,2),
    "hourly_rate" NUMERIC(10,2),
    "total_amount" NUMERIC(12,2),
    "created_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" boolean NOT NULL DEFAULT false,
    "deleted_at" timestamp NULL
);
CREATE INDEX idx_jobs_user_id ON jobs ("user_id");
CREATE INDEX idx_jobs_customer_id ON jobs ("customer_id");

-- Invoices Table
CREATE TABLE invoices (
    "invoice_id" text NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::text,
    "user_id" text NOT NULL REFERENCES "user"("user_id"),
    "job_id" text NOT NULL REFERENCES "jobs"("job_id") ON DELETE RESTRICT,
    "customer_id" text NOT NULL REFERENCES "customers"("customer_id") ON DELETE RESTRICT,
    "invoice_number" text NOT NULL,
    "invoice_date" date NOT NULL,
    "due_date" date,
    "subtotal" NUMERIC(12,2) NOT NULL,
    "tax_rate" NUMERIC(5,4) DEFAULT 0.0000,
    "tax_amount" NUMERIC(12,2) DEFAULT 0.00,
    "total_amount" NUMERIC(12,2) NOT NULL,
    "invoice_status" text NOT NULL CHECK ("invoice_status" IN ('draft', 'sent', 'paid', 'overdue', 'cancelled')) DEFAULT 'draft',
    "payment_date" date,
    "notes" text,
    "created_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" boolean NOT NULL DEFAULT false,
    "deleted_at" timestamp NULL,
    UNIQUE (user_id, invoice_number)
);
CREATE INDEX idx_invoices_user_id ON invoices ("user_id");

-- Invoice Line Items Table
CREATE TABLE "invoice_line_items" (
    "line_item_id" text NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::text,
    "invoice_id" text NOT NULL REFERENCES "invoices"("invoice_id") ON DELETE CASCADE,
    "description" text NOT NULL,
    "quantity" NUMERIC(10,2) NOT NULL,
    "unit_price" NUMERIC(12,2) NOT NULL,
    "total_price" NUMERIC(12,2) NOT NULL,
    "created_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invoice_line_items_invoice_id ON invoice_line_items ("invoice_id");