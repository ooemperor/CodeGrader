# Datamodel
In order to understand the datamodel of the CodeGrader a little bit faster you can find a listing and short description of all tables in the database (out of postgres psql)
![DataModel](images/DataModel.png)

## Tables
```
               List of relations
 Schema |       Name       | Type  |   Owner
--------+------------------+-------+------------
 public | admin_type       | table | codeGrader
 public | adminuser        | table | codeGrader
 public | attachment       | table | codeGrader
 public | evaluation_type  | table | codeGrader
 public | evaluationresult | table | codeGrader
 public | executionresult  | table | codeGrader
 public | exercise         | table | codeGrader
 public | file             | table | codeGrader
 public | instruction      | table | codeGrader
 public | membership       | table | codeGrader
 public | profile          | table | codeGrader
 public | subject          | table | codeGrader
 public | submission       | table | codeGrader
 public | task             | table | codeGrader
 public | testcase         | table | codeGrader
 public | token            | table | codeGrader
 public | user             | table | codeGrader
(17 rows)
```

## Admin Type
```
                                        Table "public.admin_type"
    Column    |           Type           | Collation | Nullable |                Default
--------------+--------------------------+-----------+----------+----------------------------------------
 id           | integer                  |           | not null | nextval('admin_type_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 name         | character varying        |           | not null |
 description  | character varying        |           |          |
Indexes:
    "admin_type_pkey" PRIMARY KEY, btree (id)
    "ix_admin_type_id" btree (id)
    "ix_admin_type_name" UNIQUE, btree (name)
Referenced by:
    TABLE "adminuser" CONSTRAINT "adminuser_admin_type_fkey" FOREIGN KEY (admin_type) REFERENCES admin_type(id)

```

## Admin User
```
                                        Table "public.adminuser"
    Column    |           Type           | Collation | Nullable |                Default
--------------+--------------------------+-----------+----------+---------------------------------------
 id           | integer                  |           | not null | nextval('adminuser_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 username     | character varying        |           | not null |
 first_name   | character varying        |           | not null |
 last_name    | character varying        |           | not null |
 email        | character varying        |           | not null |
 password     | character varying        |           | not null |
 tag          | character varying        |           |          |
 admin_type   | integer                  |           | not null |
 profile_id   | integer                  |           |          |
Indexes:
    "adminuser_pkey" PRIMARY KEY, btree (id)
    "ix_adminuser_admin_type" btree (admin_type)
    "ix_adminuser_id" btree (id)
    "ix_adminuser_profile_id" btree (profile_id)
    "ix_adminuser_username" UNIQUE, btree (username)
Foreign-key constraints:
    "adminuser_admin_type_fkey" FOREIGN KEY (admin_type) REFERENCES admin_type(id)
    "adminuser_profile_id_fkey" FOREIGN KEY (profile_id) REFERENCES profile(id)

```

## Attachment
```
                                        Table "public.attachment"
    Column    |           Type           | Collation | Nullable |                Default
--------------+--------------------------+-----------+----------+----------------------------------------
 id           | bigint                   |           | not null | nextval('attachment_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 task_id      | bigint                   |           |          |
 file_id      | bigint                   |           |          |
Indexes:
    "attachment_pkey" PRIMARY KEY, btree (id)
    "ix_attachment_file_id" btree (file_id)
    "ix_attachment_id" btree (id)
    "ix_attachment_task_id" btree (task_id)
Foreign-key constraints:
    "attachment_file_id_fkey" FOREIGN KEY (file_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    "attachment_task_id_fkey" FOREIGN KEY (task_id) REFERENCES task(id) ON UPDATE CASCADE

```

## Evaluation Type
```
                                        Table "public.evaluation_type"
    Column    |           Type           | Collation | Nullable |                   Default
--------------+--------------------------+-----------+----------+---------------------------------------------
 id           | integer                  |           | not null | nextval('evaluation_type_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 name         | character varying        |           | not null |
 description  | character varying        |           |          |
Indexes:
    "evaluation_type_pkey" PRIMARY KEY, btree (id)
    "ix_evaluation_type_id" btree (id)
    "ix_evaluation_type_name" UNIQUE, btree (name)

```

## Evaluation Result
```
                                          Table "public.evaluationresult"
      Column      |           Type           | Collation | Nullable |                   Default
------------------+--------------------------+-----------+----------+----------------------------------------------
 id               | integer                  |           | not null | nextval('evaluationresult_id_seq'::regclass)
 creation_dts     | timestamp with time zone |           | not null | now()
 updated_dts      | timestamp with time zone |           | not null | now()
 evaluation_score | double precision         |           | not null |
 submission_id    | integer                  |           |          |
Indexes:
    "evaluationresult_pkey" PRIMARY KEY, btree (id)
    "ix_evaluationresult_id" btree (id)
    "ix_evaluationresult_submission_id" btree (submission_id)
Foreign-key constraints:
    "evaluationresult_submission_id_fkey" FOREIGN KEY (submission_id) REFERENCES submission(id) ON UPDATE CASCADE

```

## Execution Result
```
                                           Table "public.executionresult"
       Column        |           Type           | Collation | Nullable |                   Default
---------------------+--------------------------+-----------+----------+---------------------------------------------
 id                  | integer                  |           | not null | nextval('executionresult_id_seq'::regclass)
 creation_dts        | timestamp with time zone |           | not null | now()
 updated_dts         | timestamp with time zone |           | not null | now()
 execution_output    | character varying        |           | not null |
 execution_exit_code | integer                  |           | not null |
 execution_duration  | double precision         |           | not null |
 submission_id       | integer                  |           |          |
 testcase_id         | integer                  |           |          |
Indexes:
    "executionresult_pkey" PRIMARY KEY, btree (id)
    "ix_executionresult_execution_duration" btree (execution_duration)
    "ix_executionresult_execution_exit_code" btree (execution_exit_code)
    "ix_executionresult_id" btree (id)
    "ix_executionresult_submission_id" btree (submission_id)
    "ix_executionresult_testcase_id" btree (testcase_id)
Foreign-key constraints:
    "executionresult_submission_id_fkey" FOREIGN KEY (submission_id) REFERENCES submission(id) ON UPDATE CASCADE
    "executionresult_testcase_id_fkey" FOREIGN KEY (testcase_id) REFERENCES testcase(id) ON UPDATE CASCADE

```

## Exercise
```
                                        Table "public.exercise"
    Column    |           Type           | Collation | Nullable |               Default
--------------+--------------------------+-----------+----------+--------------------------------------
 id           | integer                  |           | not null | nextval('exercise_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 name         | character varying        |           | not null |
 tag          | character varying        |           |          |
 subject_id   | integer                  |           |          |
 description  | character varying        |           |          |
Indexes:
    "exercise_pkey" PRIMARY KEY, btree (id)
    "ix_exercise_id" btree (id)
    "ix_exercise_name" btree (name)
    "ix_exercise_subject_id" btree (subject_id)
Foreign-key constraints:
    "exercise_subject_id_fkey" FOREIGN KEY (subject_id) REFERENCES subject(id) ON UPDATE CASCADE
Referenced by:
    TABLE "task" CONSTRAINT "task_exercise_id_fkey" FOREIGN KEY (exercise_id) REFERENCES exercise(id) ON UPDATE CASCADE ON DELETE CASCADE
```

## File
```
                                        Table "public.file"
    Column     |           Type           | Collation | Nullable |             Default
---------------+--------------------------+-----------+----------+----------------------------------
 id            | integer                  |           | not null | nextval('file_id_seq'::regclass)
 creation_dts  | timestamp with time zone |           | not null | now()
 updated_dts   | timestamp with time zone |           | not null | now()
 filename      | character varying        |           | not null |
 fileExtension | character varying        |           | not null |
 file          | bytea                    |           | not null |
Indexes:
    "file_pkey" PRIMARY KEY, btree (id)
    "ix_file_filename" btree (filename)
    "ix_file_id" btree (id)
Referenced by:
    TABLE "attachment" CONSTRAINT "attachment_file_id_fkey" FOREIGN KEY (file_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "instruction" CONSTRAINT "instruction_file_id_fkey" FOREIGN KEY (file_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "submission" CONSTRAINT "submission_file_id_fkey" FOREIGN KEY (file_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "testcase" CONSTRAINT "testcase_input_id_fkey" FOREIGN KEY (input_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "testcase" CONSTRAINT "testcase_output_id_fkey" FOREIGN KEY (output_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE

```

## Instruction
```
                                        Table "public.instruction"
    Column    |           Type           | Collation | Nullable |                 Default
--------------+--------------------------+-----------+----------+-----------------------------------------
 id           | bigint                   |           | not null | nextval('instruction_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 task_id      | bigint                   |           |          |
 file_id      | bigint                   |           |          |
Indexes:
    "instruction_pkey" PRIMARY KEY, btree (id)
    "ix_instruction_file_id" btree (file_id)
    "ix_instruction_id" btree (id)
    "ix_instruction_task_id" btree (task_id)
Foreign-key constraints:
    "instruction_file_id_fkey" FOREIGN KEY (file_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    "instruction_task_id_fkey" FOREIGN KEY (task_id) REFERENCES task(id) ON UPDATE CASCADE

```

## Membership
```
                                        Table "public.membership"
    Column    |           Type           | Collation | Nullable |                Default
--------------+--------------------------+-----------+----------+----------------------------------------
 id           | integer                  |           | not null | nextval('membership_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 user_id      | integer                  |           |          |
 subject_id   | integer                  |           |          |
Indexes:
    "membership_pkey" PRIMARY KEY, btree (id)
    "ix_membership_id" btree (id)
    "ix_membership_subject_id" btree (subject_id)
    "ix_membership_user_id" btree (user_id)
    "membership_user_id_subject_id_key" UNIQUE CONSTRAINT, btree (user_id, subject_id)
Foreign-key constraints:
    "membership_subject_id_fkey" FOREIGN KEY (subject_id) REFERENCES subject(id) ON UPDATE CASCADE
    "membership_user_id_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE

```

## Profile
```
                                        Table "public.profile"
    Column    |           Type           | Collation | Nullable |               Default
--------------+--------------------------+-----------+----------+-------------------------------------
 id           | integer                  |           | not null | nextval('profile_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 name         | character varying        |           | not null |
 tag          | character varying        |           |          |
Indexes:
    "profile_pkey" PRIMARY KEY, btree (id)
    "ix_profile_id" btree (id)
    "ix_profile_name" UNIQUE, btree (name)
Referenced by:
    TABLE "adminuser" CONSTRAINT "adminuser_profile_id_fkey" FOREIGN KEY (profile_id) REFERENCES profile(id)
    TABLE "subject" CONSTRAINT "subject_profile_id_fkey" FOREIGN KEY (profile_id) REFERENCES profile(id) ON UPDATE CASCADE
    TABLE ""user"" CONSTRAINT "user_profile_id_fkey" FOREIGN KEY (profile_id) REFERENCES profile(id)

```

## Subject
```
                                        Table "public.subject"
    Column    |           Type           | Collation | Nullable |               Default
--------------+--------------------------+-----------+----------+-------------------------------------
 id           | integer                  |           | not null | nextval('subject_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 name         | character varying        |           | not null |
 tag          | character varying        |           |          |
 profile_id   | integer                  |           |          |
Indexes:
    "subject_pkey" PRIMARY KEY, btree (id)
    "ix_subject_id" btree (id)
    "ix_subject_name" btree (name)
    "ix_subject_profile_id" btree (profile_id)
Foreign-key constraints:
    "subject_profile_id_fkey" FOREIGN KEY (profile_id) REFERENCES profile(id) ON UPDATE CASCADE
Referenced by:
    TABLE "exercise" CONSTRAINT "exercise_subject_id_fkey" FOREIGN KEY (subject_id) REFERENCES subject(id) ON UPDATE CASCADE
    TABLE "membership" CONSTRAINT "membership_subject_id_fkey" FOREIGN KEY (subject_id) REFERENCES subject(id) ON UPDATE CASCADE

```

## Submission
```
                                        Table "public.submission"
    Column    |           Type           | Collation | Nullable |                Default
--------------+--------------------------+-----------+----------+----------------------------------------
 id           | integer                  |           | not null | nextval('submission_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 file_id      | integer                  |           |          |
 user_id      | integer                  |           | not null |
 task_id      | integer                  |           | not null |
Indexes:
    "submission_pkey" PRIMARY KEY, btree (id)
    "ix_submission_file_id" btree (file_id)
    "ix_submission_id" btree (id)
    "ix_submission_user_id" btree (user_id)
Foreign-key constraints:
    "submission_file_id_fkey" FOREIGN KEY (file_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    "submission_task_id_fkey" FOREIGN KEY (task_id) REFERENCES task(id) ON UPDATE CASCADE
    "submission_user_id_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE
Referenced by:
    TABLE "evaluationresult" CONSTRAINT "evaluationresult_submission_id_fkey" FOREIGN KEY (submission_id) REFERENCES submission(id) ON UPDATE CASCADE
    TABLE "executionresult" CONSTRAINT "executionresult_submission_id_fkey" FOREIGN KEY (submission_id) REFERENCES submission(id) ON UPDATE CASCADE

```

## Task
```
                                        Table "public.task"
    Column    |           Type           | Collation | Nullable |             Default
--------------+--------------------------+-----------+----------+----------------------------------
 id           | integer                  |           | not null | nextval('task_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 name         | character varying        |           | not null |
 tag          | character varying        |           |          |
 exercise_id  | integer                  |           |          |
 description  | character varying        |           |          |
Indexes:
    "task_pkey" PRIMARY KEY, btree (id)
    "ix_task_exercise_id" btree (exercise_id)
    "ix_task_id" btree (id)
    "ix_task_name" btree (name)
Foreign-key constraints:
    "task_exercise_id_fkey" FOREIGN KEY (exercise_id) REFERENCES exercise(id) ON UPDATE CASCADE ON DELETE CASCADE
Referenced by:
    TABLE "attachment" CONSTRAINT "attachment_task_id_fkey" FOREIGN KEY (task_id) REFERENCES task(id) ON UPDATE CASCADE
    TABLE "instruction" CONSTRAINT "instruction_task_id_fkey" FOREIGN KEY (task_id) REFERENCES task(id) ON UPDATE CASCADE
    TABLE "submission" CONSTRAINT "submission_task_id_fkey" FOREIGN KEY (task_id) REFERENCES task(id) ON UPDATE CASCADE
    TABLE "testcase" CONSTRAINT "testcase_task_id_fkey" FOREIGN KEY (task_id) REFERENCES task(id) ON UPDATE CASCADE ON DELETE CASCADE

```

## Testcase
```
                                        Table "public.testcase"
    Column    |           Type           | Collation | Nullable |               Default
--------------+--------------------------+-----------+----------+--------------------------------------
 id           | integer                  |           | not null | nextval('testcase_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 input_id     | integer                  |           |          |
 output_id    | integer                  |           |          |
 task_id      | integer                  |           | not null |
Indexes:
    "testcase_pkey" PRIMARY KEY, btree (id)
    "ix_testcase_id" btree (id)
    "ix_testcase_input_id" btree (input_id)
    "ix_testcase_output_id" btree (output_id)
Foreign-key constraints:
    "testcase_input_id_fkey" FOREIGN KEY (input_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    "testcase_output_id_fkey" FOREIGN KEY (output_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
    "testcase_task_id_fkey" FOREIGN KEY (task_id) REFERENCES task(id) ON UPDATE CASCADE ON DELETE CASCADE
Referenced by:
    TABLE "executionresult" CONSTRAINT "executionresult_testcase_id_fkey" FOREIGN KEY (testcase_id) REFERENCES testcase(id) ON UPDATE CASCADE

```

## Token
```
                                        Table "public.token"
    Column    |           Type           | Collation | Nullable |              Default
--------------+--------------------------+-----------+----------+-----------------------------------
 id           | integer                  |           | not null | nextval('token_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 token        | character varying        |           | not null |
 description  | character varying        |           | not null |
Indexes:
    "token_pkey" PRIMARY KEY, btree (id)
    "ix_token_id" btree (id)
    "ix_token_token" btree (token)

```

## User
```
                                        Table "public.user"
    Column    |           Type           | Collation | Nullable |             Default
--------------+--------------------------+-----------+----------+----------------------------------
 id           | integer                  |           | not null | nextval('user_id_seq'::regclass)
 creation_dts | timestamp with time zone |           | not null | now()
 updated_dts  | timestamp with time zone |           | not null | now()
 username     | character varying        |           | not null |
 first_name   | character varying        |           | not null |
 last_name    | character varying        |           | not null |
 email        | character varying        |           | not null |
 password     | character varying        |           | not null |
 tag          | character varying        |           |          |
 profile_id   | integer                  |           |          |
Indexes:
    "user_pkey" PRIMARY KEY, btree (id)
    "ix_user_id" btree (id)
    "ix_user_profile_id" btree (profile_id)
    "ix_user_username" UNIQUE, btree (username)
Foreign-key constraints:
    "user_profile_id_fkey" FOREIGN KEY (profile_id) REFERENCES profile(id)
Referenced by:
    TABLE "membership" CONSTRAINT "membership_user_id_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE
    TABLE "submission" CONSTRAINT "submission_user_id_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE

```