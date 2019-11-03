#!/bin/sh

DEPLOY_REMOTE='origin'

DEPLOY_BRANCH_PAGES='master'
DEPLOY_BRANCH_BLOG='blog'

DEPLOY_DIR_DIST='public'
DEPLOY_DIR_CLEAN_UP=('public' 'resources')

DEPLOY_MESSAGE=$(date +'deploy on %Y-%m-%d %H:%M')

function _git()
{
    git "$@" >/dev/null 2>&1
}

function _main()
{
    _git branch -D "$DEPLOY_BRANCH_PAGES"
    _git checkout --orphan "$DEPLOY_BRANCH_PAGES"
    if [ $? -ne 0 ]
    then
        exit
    fi
    _git reset --hard
    _git commit --allow-empty -m "$DEPLOY_MESSAGE" >/dev/null 2>&1

    _git checkout "$DEPLOY_BRANCH_BLOG"
    rm -rf "${DEPLOY_DIR_CLEAN_UP[@]}"
    _git worktree add "$DEPLOY_DIR_DIST" "$DEPLOY_BRANCH_PAGES"

    hugo
    _git -C "$DEPLOY_DIR_DIST" add --all
    _git -C "$DEPLOY_DIR_DIST" commit --am --no-edit

    git -C "$DEPLOY_DIR_DIST" push --force "$DEPLOY_REMOTE" "$DEPLOY_BRANCH_PAGES"
    _git worktree remove "$DEPLOY_DIR_DIST"
    _git branch -D "$DEPLOY_BRANCH_PAGES"
}

_main