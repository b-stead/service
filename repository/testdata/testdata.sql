-- Test users
INSERT INTO
  "user" (
    "user_id",
    "sub",
    "first_name",
    "last_name",
    "email",
    "email_verified",
    "created_date",
    "is_deleted",
    "deleted_at"
  )
VALUES
  -- Brendon
  (
    'brendon-1234',
    'somerandomstring',
    'Brendon',
    'Stead',
    'brendon_stead@yahoo.com',
    TRUE,
    now(),
    False,
    NULL
  );

-- Deleted user
INSERT INTO
  "user" (
    "user_id",
    "sub",
    "first_name",
    "last_name",
    "email",
    "email_verified",
    "created_date",
    "is_deleted",
    "deleted_at"
  )
VALUES
  (
    'XkG5cTQnAlUVGdbKU0qHN0FtZv52',
    'deletedSub',
    'Deleted',
    'User',
    'deleted@test.com',
    True,
    '2024-01-01T00:00:00Z',
    TRUE,
    now()
  );

-- Test customers
INSERT INTO
  "customers" (
    "customer_id",
    "user_id",
    "name",
    "company_name",
    "organisation",
    "contact_person",
    "email",
    "phone",
    "address_line1",
    "address_line2",
    "city",
    "state",
    "postal_code",
    "country",
    "created_at",
    "is_deleted",
    "deleted_at"
  )
VALUES
  ('cust-001', 'brendon-1234', 'John Doe', 'Doe Enterprises', True, 'Jane Doe', 'john.doe@example.com', '123-456-7890', '123 Main St', 'Suite 100', 'New York', 'NY', '10001', 'USA', '2023-10-01 10:00:00', False, NULL),
  ('cust-002', 'brendon-1234', 'Alice Smith', 'Smith Consulting', False, 'Bob Smith', 'alice.smith@example.com', '987-654-3210', '456 Elm St', 'Apt 2B', 'San Francisco', 'CA', '94103', 'USA', '2023-10-02 11:00:00', False, NULL),
  ('cust-003', 'brendon-1234', 'Charlie Brown', 'Brown Logistics', False, 'Lucy Brown', 'charlie.brown@example.com', '555-123-4567', '789 Oak St', '', 'Chicago', 'IL', '60601', 'USA', '2023-10-03 12:00:00', False, NULL),
  ('cust-004', 'brendon-1234', 'Emily Davis', 'Davis & Co.', False, 'Michael Davis', 'emily.davis@example.com', '444-555-6666', '321 Pine St', 'Floor 3', 'Seattle', 'WA', '98101', 'USA', '2023-10-04 13:00:00', False, NULL),
  ('cust-005', 'brendon-1234', 'Frank White', 'White Industries', True, 'Sarah White', 'frank.white@example.com', '333-222-1111', '654 Maple St', '', 'Austin', 'TX', '73301', 'USA', '2023-10-05 14:00:00', False, NULL);

-- Test jobs
INSERT INTO
  "jobs" (
    "job_id",
    "user_id",
    "customer_id",
    "job_title",
    "job_description",
    "job_status",
    "start_date",
    "end_date",
    "estimated_hours",
    "actual_hours",
    "daily_rate",
    "hourly_rate",
    "total_amount",
    "created_at",
    "updated_at",
    "is_deleted",
    "deleted_at"
  )
VALUES
  ('job-001', 'brendon-1234', 'cust-001', 'Website Development', 'Develop a responsive website for the client.', 'completed', '2023-09-01', '2023-09-15', 80.00, 75.00, 500.00, 50.00, 3750.00, '2023-09-01 10:00:00', '2023-09-15 18:00:00', false, NULL),
  ('job-002', 'brendon-1234', 'cust-002', 'Financial Audit', 'Conduct a financial audit for the client.', 'in_progress', '2023-10-01', NULL, 40.00, NULL, 600.00, 60.00, NULL, '2023-10-01 09:00:00', NULL, false, NULL),
  ('job-003', 'brendon-1234', 'cust-003', 'Logistics Optimization', 'Optimize the logistics process for the client.', 'pending', '2023-10-10', NULL, 100.00, NULL, 700.00, 70.00, NULL, '2023-10-10 08:00:00', NULL, false, NULL),
  ('job-004', 'brendon-1234', 'cust-004', 'Legal Consultation', 'Provide legal consultation for the client.', 'cancelled', '2023-08-01', '2023-08-02', 8.00, 2.00, 1000.00, 125.00, 250.00, '2023-08-01 10:00:00', '2023-08-02 12:00:00', false, NULL),
  ('job-005', 'brendon-1234', 'cust-005', 'Manufacturing Setup', 'Set up a new manufacturing line for the client.', 'completed', '2023-07-01', '2023-07-20', 160.00, 150.00, 800.00, 80.00, 12000.00, '2023-07-01 08:00:00', '2023-07-20 18:00:00', false, NULL);