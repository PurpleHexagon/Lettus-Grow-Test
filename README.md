this is the backend software developer interview test project for LettUsGrow.
this a django project using the django rest frame work.
there is no UI. the whole focus of this is around API's and database structure.

this API is the backend for a theoretical UI tracking crops growing in a vertical farm.
allowing farmers to sow, harvest and track trays of crops as they grow.
with different species of crops growing for different lengths of time and with different yields.

there are five tasks bellow, we suggest you do them and in order however you dont have to.
if you think you can do better by "colouring out side the lines" so to speak then go for it but its probably more risky.
feel free to change absolutely ANY file. 
though you will have to justify/explain your changes...

once you are done, package this back up into a tar.gz. you have one week to complete what you can and email it back. good luck :)

you will need:  
python3.6+  
django2.2+  
markdown3.0+  


urls:  
/admin/ - the django admin screen  
/api/crop/ - the crops endpoint  
/api/growthplan/ - the growthplan endpoint  
/api/tray/ - the tray endpoint  


Tasks:  

1) get it working :)  

2) fix any failing tests.  

3) Add an estimated yield and estimated harvest date to tray data.  

4) make any improvements / fixes you think are necessary.  
   if your short on time you can add a TODO's in comments.  

5) go wild and show off your skills, add any new features you think would be good.  
   two suggestions are:  
      a) batched sowing and harvesting.  
      b) a sowing schedule with yield forecasting!!!  


Useful commands:

Up containers:
```bash
  docker-compose up
```

Create Migration:
```bash
  docker exec -it src_web_1 bash -c "python manage.py makemigrations crop"
```

Run Migrations:
```bash
  docker exec -it src_web_1 bash -c "python manage.py migrate"
```

Create Django Superuser:
```bash
  docker exec -it src_web_1 bash -c "python manage.py createsuperuser"
```

Run the tests:
```bash
  docker exec -it src_web_1 bash -c "python manage.py test"
```
