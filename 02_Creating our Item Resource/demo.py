from flask import Flask,request
from flask_restful import Resource, Api , reqparse
from flask_jwt import JWT,jwt_required

from security import authenticate,identity



app = Flask(__name__)

app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app,authenticate,identity)

items = [
    {
        'name' : 'tuan'
    }
]

class Item(Resource):
    @jwt_required()
    def get(self,name):
        # item = next(filter(lambda x : x['name'] == name , items), None)
        for item in items:
            if item['name'] == name :
                return {'item' : item}
            else:
                None 

    def post(self,name):
        # if next(filter(lambda x : x['name'] == name,items) , None):
        #     return {'message' : "An item with name '{}' aleady exis " . format(name)}
        
        for x in items :
            if x['name'] == name:
                return {'message' : "An item with name '{}' aleady exis" .format(name)}
            else :
                data = request.get_json()
                item = {
                    'name' : name , 
                    'price' : data['price']
                }
                items.append(item)
                return item

    @jwt_required
    def delete(self,name):
        global item
        items = list(filter(lambda x : x['name'] != name , items) )
        return {'message' : ' Item deleted'}

    @jwt_required
    def put(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',type = float , required = True , help = "the price is not null")
        
        data = parser.parse_args()

        # data = request.get_json() #nhap du lieu
        item = next(filter(lambda x : x['name'] == name , items) , None)
        if item is None :
            item  = {
                'name' : name,
                'price' : data['price']
            }
            items.append(item)
        else :
            item.update(data)
        return item
            

        

class ItemList(Resource):
    def get(self):
        return {'items' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')



# @app.route('/item')
# def getall():
#     return {'hello flask'}

app.run(port=5000 , debug=True)