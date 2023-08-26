from rest_framework.decorators import api_view
from rest_framework.response import Response
from study.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    rooms_serializer = RoomSerializer(rooms, many=True)
    return Response(rooms_serializer.data)


@api_view(['GET'])
def getSingleRoom(request, pk):
    rooms = Room.objects.get(id=pk)
    room_serializer = RoomSerializer(room, many=False)
    return Response(room_serializer.data)
