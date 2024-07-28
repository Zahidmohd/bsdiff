import sysconfig

include_path = sysconfig.get_path('include')
library_path = sysconfig.get_config_var('LIBDIR')
lib_name = sysconfig.get_config_var('LIBRARY')

print(f'include_path: {include_path}')
print(f'library_path: {library_path}')
print(f'lib_name: {lib_name}')
