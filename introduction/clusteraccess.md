## 🔐 Accessing CHESS Computing Resources
Follow the steps below to log in and start an interactive session on the CHESS cluster.

#### ✅ Step 1: Open Your Terminal

On Mac/Linux: Open the Terminal application
On Windows: Use PowerShell, Command Prompt, or tools like Git Bash


#### ✅ Step 2: Connect via SSH
In your terminal, type the following command:
Shellssh <username>@lnx201.classe.cornell.eduShow more lines
👉 Replace <username> with your assigned CLASSE username
Example:
Shellssh js1234@lnx201.classe.cornell.eduShow more lines
📌 You may be prompted to:

Accept the host key (type yes)
Enter your password

#### ✅ Step 3: Start an Interactive Job Session
Once logged in, run:
Shellqrsh -q interactive.q -l mem_free=200G -pe sge_pe 8``Show more lines

✅ What This Command Does
qrsh → starts an interactive job session
-q interactive.q → selects the interactive queue
-l mem_free=200G → requests 200 GB RAM
-pe sge_pe 8 → requests 8 CPU cores


#### ✅ Step 4: Wait for Job Allocation

The system will allocate resources
Once ready, your prompt will update
You are now running on a compute node 🎉

#### ✅ Step 6: Activate your oqn environment

✅ Step 5: Start Your Work
You can now:
Run Python scripts
Use Jupyter notebooks
Process synchrotron data
Execute training jobs


⚠️ Important Notes
[!WARNING]
Activate your own environment

[!IMPORTANT]
Always request only the resources you need to avoid long wait times.


[!TIP]
If your job takes too long to start, consider requesting fewer resources.


[!WARNING]
Do not run heavy computations directly on the login node (lnx201).


