### Generating a report

Esi-Leap along with the python-esi-leap client allow the user to easily generate reports on usage
of a resource over time.

To generate a csv file with data on all lessees' usage on different nodes:
```
openstack lease contract list --all --long -f csv > report.csv
```

The Esi-Leap api allows users to retrieve data based on certain parameters. 

For example, it is possible to generate a report based on a lessee's openstack project_id. To get a list of all
projects type ``openstack project list`` and from there grab the desired project id and run the command:


```
openstack lease contract list --project-id <project_id> --all --long -f csv > report.csv
```

To generate a report based on usage of a particular owner's resources, run the command:

```
openstack lease contract list --owner <project_id> --all --long -f csv > report.csv
```

To generate a report based on usage over a particular date range, run the command:

```
opensack lease contract list --time-range <datetime string> <datetime string> --all --long -f csv > report.csv
```

These different arguments can be combined together for report generation.
