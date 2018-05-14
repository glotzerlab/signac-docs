{% for operation in operations %}
mpiexec -n {{ operation.directives.np }} {{ operation.cmd }}
{% endfor %}
