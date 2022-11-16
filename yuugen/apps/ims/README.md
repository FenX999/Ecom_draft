#Inventory App
##this app cover the inventory side of the ecommerce.

###how it work

Each product in the front end has a SKU define who play the role of parent
Ex: for a product named Hadoken the SKU will be SKU_hadoken

if the product as mutliple color then a child of the SKU should be created for each color available 
EX: if black is part of the attribute color the the new SKU should be SKU_hadokem_black

same with sizes if exists the new SKU should recall the product name then the color if exists and the size,

Ex: SKU_+<product>+<color>+<size>


that way you have full control of your inventory by color ( sum of all size ) by size ( sum of all color ) or by individual reference of a product 
ex SKU_hadoken_black_xl has 999 units inside the 49999 units that the Product Hadoken has in inventory 

for now all of the SKU are manuel to maintain the finished project as a whole a priority



