# ARRAY / LAB — NumPy Array Operations (Task 12)

A responsive mini web app for entering two numerical arrays and calculating element-wise addition, subtraction, multiplication, and division using **Python + NumPy**. The server uses Python's built-in `http.server`; no Flask, notebook, database, or paid service is required.

## Features
- Create two arrays using comma-separated values.
- NumPy-backed vectorized arithmetic.
- Validates numeric input and matching array lengths.
- Handles division by zero safely by displaying `undefined`.
- Responsive custom UI and sample data presets.
- `/health` endpoint for deployment health checks.

## Requirements
- Python 3.10 or newer
- Internet connection for the first NumPy installation only

## Run from the terminal (Windows PowerShell)

1. Extract `task12_numpy_array_operations.zip`.
2. Open PowerShell and move into the extracted folder. Example:

   ```powershell
   cd "$HOME\Downloads\task12_numpy_array_operations"
   ```

   If you extracted it elsewhere, use that folder's actual path.

3. Check Python:

   ```powershell
   py --version
   ```

4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it. If PowerShell blocks activation, use the no-policy-change alternative below.

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **If activation is blocked**, you do not need to change the computer's execution policy. Run pip and Python directly from the virtual environment:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe app.py
   ```

   If activation works, instead run:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python app.py
   ```

6. Open this address in your browser: **http://127.0.0.1:8000**
7. Try the default values or choose a sample from the menu. To stop the server, return to PowerShell and press `Ctrl+C`.

If port 8000 is already occupied, start with another port:
```powershell
$env:PORT=8001
.\.venv\Scripts\python.exe app.py
```
Then open `http://127.0.0.1:8001`.

## Example test data

Array A: `12, 24, 36, 48`  
Array B: `3, 6, 9, 12`

- Addition: `[15, 30, 45, 60]`
- Subtraction: `[9, 18, 27, 36]`
- Multiplication: `[36, 144, 324, 576]`
- Division: `[4, 4, 4, 4]`

Other tests:
- Decimals: A=`1.5, 2.75, 8.2`; B=`0.5, 1.25, 2`
- Negative values: A=`-5, 10, -15`; B=`2, -4, 3`
- Zero division: A=`10, 20, 30`; B=`2, 0, 5`
- Invalid shape: A=`1, 2, 3`; B=`4, 5` (should show a validation message)
- Invalid input: A=`1, hello, 3`; B=`4, 5, 6` (should show a validation message)

## How vectorization works
`np.add(a, b)`, `np.subtract(a, b)`, `np.multiply(a, b)`, and `np.divide(a, b)` apply arithmetic element-wise across the arrays. This avoids writing an explicit Python loop and is a core reason NumPy is convenient for numerical work. For this task, both arrays must have the same shape.

## Deploy on Render (optional)
The repository includes `render.yaml` as deployment configuration.

1. Push this project to a **public GitHub repository**.
2. Sign in to Render and choose **New + → Blueprint**.
3. Connect the GitHub repository containing `render.yaml`.
4. Review the service settings and deploy.
5. When deployment finishes, open the Render URL and test the calculator and `/health`.

Free service availability and terms can change. If Blueprint is not offered on your account, create a Web Service manually with build command `pip install -r requirements.txt` and start command `python app.py`.

## GitHub: create and push a repository

Create a new repository here: https://github.com/new

Suggested repository name: `task12-numpy-array-operations`

- Choose **Public** (required by the task instructions).
- Do not initialize it with a README, `.gitignore`, or license, because these files already exist in this project.

In PowerShell, from the extracted project folder, run these commands in order:

```powershell
git --version
git init
git add .
git status
git commit -m "Build Task 12 NumPy array operations web app"
git branch -M main
git remote add origin https://github.com/PranathiM15/task12-numpy-array-operations.git
git push -u origin main
```

If GitHub shows a different username or you chose a different repository name, replace the URL with the HTTPS URL shown on the repository page.

### Avoid common GitHub push errors
- **`git` is not recognized:** install Git for Windows from https://git-scm.com/download/win, then reopen PowerShell.
- **`remote origin already exists`:** run `git remote -v`; then use `git remote set-url origin https://github.com/PranathiM15/task12-numpy-array-operations.git`.
- **`src refspec main does not match any`:** make sure `git add .` and `git commit` completed successfully before pushing.
- **Authentication prompt:** complete the browser sign-in flow. GitHub account passwords are not accepted for Git HTTPS pushes.
- **Rejected because remote contains work:** if you accidentally initialized the remote with a README, do not force push. Create a fresh empty repository or ask for help resolving the histories safely.

## Rollback evidence
For a simple rollback demonstration, make a small change to `README.md`, commit it, then revert that commit:

```powershell
git add README.md
git commit -m "Document a small update"
git log --oneline -3
git revert HEAD
git log --oneline -3
git status
```

The `git revert` command creates a new commit that undoes the previous commit without rewriting history. Capture terminal screenshots of the commit log before and after the revert and include them in your submission. Do not run `git reset --hard` on your only copy.

## Suggested screenshots for submission
1. Main page showing both arrays and all four results.
2. Decimal sample.
3. Division-by-zero sample showing `undefined`.
4. Validation error for arrays with different lengths.
5. PowerShell terminal with the app running.
6. GitHub repository page showing committed files.
7. Deployment page/URL if deployed.
8. Terminal `git log` showing the rollback/revert commits.

## Project structure
```text
task12_numpy_array_operations/
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
└── .gitignore
```
