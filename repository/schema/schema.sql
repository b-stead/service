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

