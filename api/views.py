from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Note
from .serializers import NoteSerializer

# Create your views here.

@api_view(['GET'])
def getRoutes(routes):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def getNotes(request):
    notes= Note.objects.all().order_by('-updated')
    serializer =NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getNote(request,pk):
    notes= Note.objects.get(id=pk)
    serializer =NoteSerializer(notes, many=False)
    return Response(serializer.data)
# @api_view(['GET'])
# def getNotes(request):
#     if request.method == 'GET':
#         notes = Note.objects.all()
#         serializer = NoteSerializer(notes, many=True)
#         return Response(serializer.data)

    # elif request.method == 'POST':
    #     data = request.data
    #     note = Note.objects.create(body=data.get('body', ''))
    #     serializer = NoteSerializer(note, many=False)
    #     return Response(serializer.data)

# @api_view(['GET'])
# def getNotes(request):
#     notes= Note.objects.all()
#     serializer =NoteSerializer(notes, many=True)
#     return Response(serializer.data)

# @api_view(['PUT','DELETE'])
# def updateOrDeleteNotes(request, pk):
#     if request.method == 'PUT':
#         try:
#             if pk == 'new':
#                 data = request.data
#                 note = Note.objects.create(body=data['body'])
#                 serializer = NoteSerializer(note, many=False)
#                 return Response(serializer.data)

#             note = Note.objects.get(id=pk)
#             serializer = NoteSerializer(instance=note, data=request.data)
        
#             if serializer.is_valid():
#                 # continue your code here        




@api_view(['POST'])
def createNote (request):
    data = request.data
    note = Note.objects.create(
        body=data['body']
    )
    serializer =NoteSerializer(note, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updateNote(request, pk):
    try:
        if pk == 'new':
            # Handle creation of a new note here
            data = request.data
            note = Note.objects.create(body=data['body'])
            serializer = NoteSerializer(note, many=False)
            return Response(serializer.data)

        # Continue with the normal update logic for existing notes
        note = Note.objects.get(id=pk)
        serializer = NoteSerializer(instance=note, data=request.data)
        
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=404)
    except Exception as e:
        print(f"Error updating note: {e}")
        return Response({'error': 'Internal Server Error'}, status=500)

@api_view(['DELETE'])
def deleteNote(request,pk):        
    try:
        note=Note.objects.get(id=pk)
        note.delete()
        return Response('Note was deleted')
    except Note.DoesNotExist:
        return Response({'error':'Note not found'}, status=404)