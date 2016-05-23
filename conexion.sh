#!/bin/sh

id=$1
agencia=$2
fecha=$3
hora=$4
latitud=$5
longitud=$6
dep=$7
mag=$8
region=$9

echo $id" "$agencia" "$fecha" "$hora" "$latitud" "$longitud" "$dep" "$mag" "$region




#### Defino los parametros de conexión a la BD mysql
sql_host="10.100.100.202"
slq_usuario="preliminar"
sql_password="preliminar"
sql_database="preliminar"
### Se monta los parámetros de conexión
sql_args="-h $sql_host -u $slq_usuario -p$sql_password -D $sql_database -s -e"
### Mi sentencia Sql para que la muestre
mysql $sql_args "insert into internacionales(id,agencia,fecha,hora,latitud,longitud,profundidad,magnitud,epicentro)values('$id','$agencia','$fecha', '$hora','$latitud','$longitud','$dep','$mag','$region')";

