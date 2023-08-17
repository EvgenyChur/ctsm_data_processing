# ctsm_data_processing
Repository has scripts for pre- and post- processing of data for CTSM model



## Content of ctsm_data_processing repository:
Project has 2 main folders:
1. `scripts` -> has modules for pre- and post- processing of CTSM data in NetCDF format.
    - ***check_input_forcing.py*** -> script for initial evaluating B1850 forcing data;
    - ***check_spinup_data.py*** -> script for evaluating CTSM Spinup data;
    - ***compare_forcing.py*** -> script for comparison of GSWP3 and B1850 forcing data for CTSM model;
    - ***config.py*** -> user settings for linear plots;
    - ***lib4sys_support.py*** -> module with personal functions for work with system;
    - ***lib4visualization.py*** -> module with personal functions for work visualization;
    - ***prep_forcing_cesm.bash*** -> *shell* script for initial preprosessing B1850 forcing data;
    - ***prep_forcing_gswp3.bash*** -> *shell* script for initial preprosessing GSWP3 forcing data;
    - ***prep_forcing4comparison.bash*** -> *shell* scrip for processing B1850 data;

2. `RESULTS` -> examples of output figures;

3. `README.md` -> current file;

4. `LICENSE`

5. DOCS -> documentation, how to run CTSM model on LEVANTE cluster;

## Cloning ctsm_data_processing processing scripts:
In order to use/develop ctsm_data_processing scripts, repository should be cloned. To clone from gitlab, you need to provide a valid public key or use HTTPS connection. In the latter case, you have to write your login and password everytime when you want to do something with gitlab server. More information is available on the official gitlab web-page ([how to use SSH keys to communicate with Github][2]):

If you want to continue developing of *ctsm_data_processing* scripts you have to do the next things:
1. Open the web version of *ctsm_data_processing* project and create `a new issue` with the name of your research or task. Name should gives other users the key aspect of your work;
2. From your new issue, you have to create a new branch with the name **/feature/{direction_of_your_updates}**. You have to use a branch `main` as a source branch;
3. At the moment, your new branch is a full copy of the main branch and you can clone it to your "local" computer:
```
git clone --branch /feature/{direction_of_your_updates} https://github.com/EvgenyChur/ctsm_data_processing.git CESM_PROCESSING
cd CESM_PROCESSING
git status
```
4. If you want to add changes into ctsm_data_processing scripts you have to use these commands:
```
git status
git add *
git commit -m 'your commit name'
git push
```
Now all your changes are visible in web-version and you can check them.
5. If you want to `merge` your updates to the main branch you have to `create a new merge reguest`;
6. Sometimes, you branch can have the older version that the source branch and if you want to update your branch to the last version of source branch you can use:
```
git pull
```
However, your updates will be replaced by the updated version. More information about git command you can find in Google!


***P.S.1: You have to change these name {direction_of_your_updates} and {your commit name} to yours***

***P.S.2: Don't forget that before you start working with ctsm_data_processing scripts on MPI-BGC SLURM cluster or your local computer, you have to plug SLURM modules, install and set your enviroments for miniconda (anaconda), set git parameters (user.name and user.email), set a valid public key for GitLab. More information about you can find in MPI-BGC discourse. The main useful links are presented in section Additional materials***

## Additional materials:
There are a lot of useful information in MPI-BGC discourse platform for communication. For example:
1. **BGC SLURM cluster**:
    - [Introduction to BGC slurm-cluster][9]
    - [BGC slurm-cluster basics][10]
    - [Basic introduction to the BGC slurm-cluster][11]

2. **Python instructions**:
    - [Setting up Python/IPython/Jupyter on the slurm-cluster][6]
    - [Python code publishing recipes and info][7]
    - [How-to embarassingly parallel Python Jobs on BGC Slurm cluster][8]

3. **Git usage tutorials**:
    - [General information about git][3] and more detailed discussion [how to use gitlab on MPI-BGC cluster][4];
    - [Using Github on MPI-BGC cluster][5];

Don't forget to get access to MPI-BGC Discourse.

[link1]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/blob/Version_19082022/REPORTS/RECCAP2-A_Protocol.docx
[link2]: https://climate.esa.int/en/projects/reccap-2/

[2]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
[3]: https://bgc.discourse.mpg.de/t/git-usage-tutorial/40
[4]: https://bgc.discourse.mpg.de/t/git-usage-tutorial-discussion/3049
[5]: https://bgc.discourse.mpg.de/t/using-github-on-cluster-development-nodes/3711
[6]: https://bgc.discourse.mpg.de/t/setting-up-python-ipython-jupyter-on-the-slurm-cluster/2975
[7]: https://bgc.discourse.mpg.de/t/python-code-publishing-recipes-and-info/2132
[8]: https://bgc.discourse.mpg.de/t/how-to-embarassingly-parallel-python-jobs-on-bgc-slurm-cluster/3691
[9]: https://bgc.discourse.mpg.de/t/introduction-to-bgc-slurm-cluster/3142
[10]: https://bgc.discourse.mpg.de/t/bgc-slurm-cluster-basics/3482
[11]: https://bgc.discourse.mpg.de/t/basic-introduction-to-the-bgc-slurm-cluster/3663

## Errors:
1. You can get this error -> `PuTTY X11 proxy: unable to connect to forwarded X server: Network error: Connection refused`. Don't panic the main problem is that figure cannot be open on MPI-BGC cluter. To fix it, you can install Xming or open the figure later. This problem is common for Windows system;