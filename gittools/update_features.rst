Let us say we are developping many features and a merge request occurs in master.

So i pull master and run the autorebase script, i had my feature branches rebased ok and i had to

.. code-block::
    git branch --contains master | grep -v '^\*'
    #checks the branch i will have to push
    git branch --contains master | grep -v '^\*' | xargs git push origin -f
    #Ok these were my features branches push them -f

I had thre branch i was the only commiter in,
so after a quick check i could push -f beign sure not to lose any commit.

The real solution is to run autorebase on the remote host, then all problems are solved :)


I suggest we compare feature and origin/feature, if it's ok we may automatically
rebase on master then push -f

.. code-block::
    for feature in $(git branch --contains master | cut -c 3- | grep -v "^master$")
        # Cut removes star, whitepsace and master branch
        if feature' in $(git branch --contains origin/feature):
            git rebase master feature
            git push -f feature
