import os
import click
import os
import clarifai
from git import Repo
import json
import sys
#this is unfisheed work in progress to do the git dump in python.
# we are using scripts/prepare_git.sh so this is for later.

def iprint(x):
    print(x)
    print(dir(x))
    print(id(x))
    print(type(x))

@click.command()
@click.option('--repo-path', default=".", help='Path to Git Repository')
@click.option('--output-file', help='Output file to store JSON data')
def main(repo_path, output_file):
    repo = Repo(repo_path)
    print(repo)
    print(repo.index)
    print(dir(repo.index))
    for x in repo.index.iter_blobs():
        print(x)
        print(x.count)
        print(x.index)
        iprint(x)
        #['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index']
        
    # ['Index', 'S_IFGITLINK', '_VERSION', '__abstractmethods__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '_abc_impl', '_commit_editmsg_filepath', '_delete_entries_cache', '_deserialize', '_entries_for_paths', '_entries_sorted', '_extension_data', '_file_path', '_flush_stdin_and_wait', '_index_path', '_items_to_rela_paths', '_iter_expand_paths', '_preprocess_add_items', '_process_diff_args', '_read_commit_editmsg', '_remove_commit_editmsg', '_serialize', '_set_cache_', '_store_path', '_to_relative_path', '_write_commit_editmsg', '_write_path_to_stdin', 'add', 'checkout', 'commit', 'diff', 'entries', 'entry_key', 'from_tree',
    #'iter_blobs', 'merge_tree', 'move', 'new', 'path', 'remove', 'repo', 'reset', 'resolve_blobs', 'unmerged_blobs', 'update', 'version', 'write', 'write_tree']
    
    print(repo.head)
    print(repo.heads)
    print(dir(repo))
    #['DAEMON_EXPORT_FILE', 'GitCommandWrapperType', '__annotations__', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_bare', '_clone', '_common_dir', '_config_reader', '_get_alternates', '_get_config_path', '_get_untracked_files', '_set_alternates', '_to_full_tag_path', '_working_tree_dir',
    # 'active_branch', 'alternates', 'archive', 'bare', 'blame', 'blame_incremental',
    # 'branches', 'clone', 'clone_from', 'close', 'commit', 'common_dir', 'config_level',
    # 'config_reader', 'config_writer', 'create_head', 'create_remote', 'create_submodule', 'create_tag',
    #'currently_rebasing_on', 'daemon_export', 'delete_head', 'delete_remote', 'delete_tag',
    #'description', 'git', 'git_dir', 'has_separate_working_tree', 'head', 'heads',
    #'ignored', 'index', 'init',
    # 'is_ancestor', 'is_dirty', 'is_valid_object', 'iter_commits', 'iter_submodules', 'iter_trees', 'merge_base', 'odb', 're_author_committer_start', 're_envvars', 're_hexsha_only', 're_hexsha_shortened', 're_tab_full_line', 're_whitespace', 'references', 'refs', 'remote', 'remotes', 'rev_parse', 'submodule', 'submodule_update', 'submodules', 'tag', 'tags', 'tree', 'unsafe_git_clone_options', 'untracked_files', 'working_dir', 'working_tree_dir']
    
    #all_objects = list(repo.iter_objects())
    #for git_object in all_objects:
    #    object_content = git_object.data_stream.read()
        #clarifai_api.inputs.create_bytes(object_content)
    #    data = {
     #       'object_name': git_object.name,
     #       'object_type': str(type(git_object)),
            # Add more data fields as needed
     #   }
        
        # Serialize data to JSON and store as a single line
        #json_data = json.dumps(data)
        #output_file.write(json_data + '\n')
        #print(json_data)
        
if __name__ == '__main__':
    main()


