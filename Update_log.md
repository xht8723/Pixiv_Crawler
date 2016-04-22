2016-04-16 Created the repo and the prototype is done.

           Problems encountered:
                      1. The algorithm for searching marked Users' id needs is lack of presicion. (It will search other users id appears on the page like: yourself and other 'recomended users')
                      2. Time efficiency.

2016-04-17 script completed.

           Problems encountered:
                      Lethally, pixiv.net protects its image being visited from outside. you can only access the image source link thru pixiv.net

2016-04-20 Header added. Fixed the problem that pixiv preventing outside visit.

           Problems encountered:
                      The downloaded picture is broken for some reason. Suspecting encoding problem.

2016-04-20 Scripted completed all problems fixed.

           Things needs to improve:
                      1. This one is only for my personal use.
                      2. Only the first page work of your followed artist will be downloaded.
                      3. Bad style :P


2016-04-20 Fixed the no.2 problem in the update above. Now all images of all pages will be downloaded.

           Things remain:
                      1. Personal use still
                      2. super bad style now qq.
                      3. Can't download Manga style page.
                      4. I'm not sure how long will single login cookie last. The program needs to be able to refresh login cookie before it expire if downloading takes too much time.

2016-04-20 Find a mysterious bug causing recorded users number reduced.
           Added a Check_number.py to check the number of users and illust id.

           Things to do:
                      1. Fix the bug mentioned.
                      2. Still, bad style QQ.
                      3. Find a way to save time...

2016-04-22 Added duplicate check so that when you run it second time, it won't download those pictures that already exist.
           Did some memory cleaning before download.

           Things to do:
                      1. Find a way to save time.
                      2. GUI(maybe)
                      3. needs to add a cookie refresh function.
                      4. Add a program that can randomly select a few image.(well, I don't think I will ever browse these 20k images...so i just randomly select some everyday.)
                      5. Using Sina weibo, Tencent weibo and twitter's API to create a image sending program.

2016-04-22 Added cookie header generator and user cmd input id and password, everybody can use the script now! ;)

           Things to do:
                      1. Find a way to save time.
                      2. GUI(maybe)
                      3. Add a program that can randomly select a few image.(well, I don't think I will ever browse these 20k images...so i just randomly select some everyday.)
                      4. Using Sina weibo, Tencent weibo and twitter's API to create a image sending program.
