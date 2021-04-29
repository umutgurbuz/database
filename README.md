# database

Case 1
-Ubuntu 20.04'e Docker kurdum.
-Alttaki komut ile docker imageını çektim, ondan node1 adında bir konteynır yarattım ve arka planda çalıştırdım.
docker run -d --name node1 -p 8091-8096:8091-8096 -p 11210-11211:11210-11211 couchbase
Aşağıdaki komut ile node1'ın shelline girdim, çünkü işlemleri couchbase cli ile yapmak istiyordum. Bu aşamada serverın çalıştığını localhost:8091'i ziyaret ettiğimde görebiliyordum.
docker container exec -it node1 /bin/bash
aşağıdaki komutla node1 isimli bir cluster oluşturdum.
couchbase-cli cluster-init -c 172.17.0.2 \
--cluster-username node1 \
--cluster-password password \
--services data,index,query \
--cluster-ramsize 512 \
--cluster-index-ramsize 256
Artık clusterıma bucket ekleyebilir, o bucketlarda dökümanlar oluşturabilirim. Aynı zamanda scale etmek adına yeni nodelar da ekleyebilirim. Alttaki komutları kullanarak travel-sample ve beer-sample örnek bucketlarını ekledim.
cbdocloader -c localhost:8091 -u node1 -p password -b travel-sample -m 256 -d /opt/couchbase/samples/travel-sample.zip
cbdocloader -c localhost:8091 -u node1 -p password -b beer-sample -m 256 -d /opt/couchbase/samples/beer-sample.zip
Ardından node2 isminde bir konteynır daha oluşturdum ve çalıştırdım.
sudo docker run -d --name node2 -p 9091-9096:8091-8096 -p 21210-21211:11210-11211 couchbase
Sonrasında aşağıdaki iki komut ile yeni node'u önceden oluşturduğum cluster'a ekledim ve rebalance ettim.
couchbase-cli server-add -c 172.17.0.2:8091 --username node1 --password password
--server-add http://172.17.0.3:8091 --server-add-username user --server-add-password password --services data
couchbase-cli rebalance -c 172.17.0.2 --username node1 --password password
Bizden hem SQL hem de key-value sorguları yapılabilcek bi sistem istenmiş. Bunlar sırasıyla couchbase serverın query ve data servisleri ile yapılıyor. İkini node'umu eklerken query servisiyle olusturmadıgım için aşağıdaki komutla node'u kaldırıp query servisi ile yeniden cluster'a ekledim ve yeniden rebalance ettim. couchbase-cli rebalance
couchbase-cli rebalance --cluster=172.17.0.2:8091 --username node1 --password password --server-remove=172.17.0.3
couchbase-cli server-add -c 172.17.0.2:8091 --username node1 --password password --server-add http://172.17.0.3:8091 --server-add-username user --server-add-password password --services data,index,query
couchbase-cli rebalance -c 172.17.0.2 --username node1 --password password
Case 2
couchbase_server classlarından oluşturduğum objelerden çağırdığım fonksiyonla, /pools/default/buckets endpointine
get requesti attığım bir kod yazdım. Aynı şekilde diğer endpointler için de fonksiyonlar eklenebilir.
