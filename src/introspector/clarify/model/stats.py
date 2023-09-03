import pstats
import os
ps = pstats.Stats('out.perf')
dd = ps.sort_stats(pstats.SortKey.CUMULATIVE)
#print(dd.__dict__)
#{'stream': <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>, 'all_callees': None, 'files': ['Sat Sep  2 09:08:19 2023    out.perf'], 'fcn_list': [('~'
import pkg_resources

def find_package_name(file_path):
    # Use pkg_resources to find the package name containing the file.
    try:
        package = pkg_resources.get_distribution(file_path)
        return package.project_name
    except pkg_resources.DistributionNotFound:
        return None
for x in dd.fcn_list:

    file_path = x[0]
    if file_path != "~":
        if not os.path.exists(file_path):
            continue
        print(file_path)
        #package_name = find_package_name(file_path)
        #print(file_path, package_name)
#.print_stats(2000)
