




#  def createNote (request):
#      data = request.data
#      note = Note.objects.create(
#          body=data['body']
#      )
#      serializer =NoteSerializer(note, many=False)
#      return Response(serializer.data)