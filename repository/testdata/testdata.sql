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