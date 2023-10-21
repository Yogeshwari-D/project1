from django.shortcuts import render
import pandas as pd
import json
import asyncio
from django.http import JsonResponse, HttpResponse
from .models import Candle

async def process_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        timeframe = int(request.POST.get('timeframe', 1))
        uploaded_file = request.FILES['csv_file']

        df = pd.read_csv(uploaded_file)
        df['date'] = pd.to_datetime(df['date'])
        candles = df.to_dict(orient='records')

        # Define your candle conversion logic here

        # Save the converted data to a JSON file
        json_data = json.dumps(candles)
        with open('converted_data.json', 'w') as json_file:
            json_file.write(json_data)

        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="converted_data.json"'

        return response

    return JsonResponse({'error': 'Invalid request'})


