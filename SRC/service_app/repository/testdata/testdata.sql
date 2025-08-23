-- Test users
INSERT INTO
  "user" (
    "user_id",
    "sub",
    "first_name",
    "last_name",
    "email",
    "email_verified",
    "created_date"
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
    '2024-01-01T00:00:00Z'
  );