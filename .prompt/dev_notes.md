# dev_notes.md

## Step 1
**Prompt used:** "Open VS Code with Copilot enabled."
**Notes:** Copilot installed and visible in sidebar; no issues.

## Step 2
**Prompt used:** "Initialize git and create README; connect to GitHub."
**Notes:** Needed to fix remote URL; after browser sign-in, push succeeded.

## Step 3
**Prompt used:** "Create Employee class with validation (names, 3-letter dept, 10-digit phone)."
**Notes:** Worked; added stricter regex for names/spaces.

## Step 4
**Prompt used:** "Make id read-only; format phone as (XXX)XXX-XXXX; add minimal tests."
**Notes:** Implemented via no setter for id; stored digits and formatted on read.

## Step 5
**Prompt used:** "Write load_employees/save_employees for CSV; add create/edit/delete/display."
**Notes:** Ensured CSV header handling and duplicate-ID guard; display output matches spec.

## Step 6
**Prompt used:** "Menu-based CLI (Add/Edit/Delete/List/Quit) calling storage functions."
**Notes:** Kept all validation in Employee; UI just catches exceptions.
