from django.db import models


class Country(models.TextChoices):
    
    NIGERIA = "NIGERIA", "Nigeria"
    UK = "UK", "United Kingdom"
    USA = "USA", "United States of America"
    GHANA = "GHANA", "Ghana"
    
    
    
class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    CLIENT = "CLIENT", "Client"
    SKILLAS = "SKILLAS", "Skillas"
    COMPANY = "COMPANY", "Company"
        
        
        
class SkillLevel(models.TextChoices):
    LEVEL_1 = "BEGINNER", "Beginner"
    LEVEL_2= "INTERMEDIATE", "Intermediate"
    LEVEL_3 = "EXPERT", "Expert"
	
        
        
class Rate(models.IntegerChoices):
    STAR_1 = 1, "1"
    STAR_2 = 2, "2"
    STAR_3 = 3, "3"
    STAR_4 = 4, "4"
    STAR_5 = 5, "5"


 
class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_PROGRESS = "IN_PROGRESS", "In progress"
    COMPLETED = "COMPLETED", "Completed"
    
    
    
    
    
# <body class="bg-white font-family-karla h-screen">
           
#         <div class="md:flex pt-16 justify-between item-center">

#             <div class="big-rose-300 px-16 md:w-1/2">
#                 <img src="{% static '/img/community.jpg' %}">
#             </div>
        
#             <div class="md:w-1/2 pr-8">
#                 {% if messages %}
#                 <ul class="messages">
#                     {% for message in messages %}
#                     <li {% if message.tags %} class="{{ message.tags }} bg-green-600 text-white text-center font-bold"{% endif %}>{{ message }}</li>
#                     {% endfor %}
#                 </ul>
#                 {% endif %}
                
#                 <form method="POST" class="bg-white rounded-lg px-8 pt-6 pb-8 mb-4">
#                     {% csrf_token %}
#                     <div class="text-2xl px-1 text-gray-700 font-semibold">
#                     Sign Up
#                     </div>

#                     <br>

#                     <div class="mb-4">
#                         <label class="block text-gray-700 text-sm font-bold mb-2">
#                                 Username
#                         </label>
#                     <input name="username"
#                         class="shadow appearance-none border border-blue-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username">
#                     </div>

#                     <div class="mb-4">
#                         <label class="block text-gray-700 text-sm font-bold mb-2">
#                                 First name
#                         </label>
#                         <input name="first_name"
#                             class="shadow appearance-none border border-blue-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="First name">
#                     </div>

#                     <div class="mb-4">
#                         <label class="block text-gray-700 text-sm font-bold mb-2">
#                                 Last name
#                         </label>
#                     <input name="last_name"
#                         class="shadow appearance-none border border-blue-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Last name">
#                     </div>

#                     <div class="mb-4">
#                         <label class="block text-gray-700 text-sm font-bold mb-2">
#                                 Email
#                         </label>
#                     <input name="email"
#                         class="shadow appearance-none border border-blue-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Email">
#                     </div>

#                     <div class="mb-4">
#                         <label class="block text-gray-700 text-sm font-bold mb-2">
#                                 Phone number
#                         </label>
#                     <input name="phone_no"
#                         class="shadow appearance-none border border-blue-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" placeholder="phone">
#                     </div>

#                     <div class="mb-4">
#                             <label for="id_role" class="block text-gray-700 text-sm font-bold mb-2">
#                                 Role
#                             </label>
#                             <select name="role" required="" id="id_role">

#                         <option value="" selected="">Chose an option</option>
                        
#                         {% comment %} <option value="ADMIN">Admin</option> {% endcomment %}
                        
#                         <option value="CLIENT">Client</option>
                        
#                         <option value="SKILLAS">Skillas</option>
                        
#                         <option value="FACILITATOR">Facilitator</option>
                        
#                         </select>
#                     </div>


#                     <div class="mb-4">
#                             <label class="block text-gray-700 text-sm font-bold mb-2">
#                                 Password
#                             </label>
#                         <input name="password1"
#                             class="shadow appearance-none border border-blue-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="myInput" type="password" placeholder="Password should be longer than 7 characters and must contain at least symbol, an uppercase letter and number">
#                     </div>
#                     <div class="mb-6">
#                         <label class="block text-gray-700 text-sm font-bold mb-2">
#                                 Confirm Password
#                         </label>
#                         <input name="password2"
#                             class="shadow appearance-none border border-purple-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="password2" type="password" placeholder="******************">

#                             <input class="border border-blue-500 rounded" type="checkbox" onclick="myFunction()"> Show Password
#                     </div>
#                     <div class="md:flex items-center justify-between">
#                         <button type="submit"
#                             class="bg-blue-900 w-full hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">
#                             Register
#                         </button>
                        
#                     </div>
                    
#                 </form>

#                 {% comment %} <form>
#                     {% csrf_token %}
                
#                       {{ form.as_p }}
                
#                       <button type="submit"
#                         class="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-sm border-4 text-white py-1 px-2 rounded"
#                         type="button">
#                         Sign Up

#                       </button>
                
#                 </form> {% endcomment %}
                
#             </div>            
            
#         </div>

      
#         <script>
#             function myFunction() {
#               var x = document.getElementById("myInput");
#               var y = document.getElementById("password2");
#               if (x.type === "password" && y.type === "password") {
#                 x.type = "text";
#                 y.type = "text";
#               } else {
#                 x.type = "password";
#                 y.type = "password"
#               }
#             }
#             </script>
#     </body>