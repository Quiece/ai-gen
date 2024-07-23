import requests
import json
from .payloads import *

class PixaiTask:
    def __init__(self, api, task_id):
        self.api = api
        self.task_id = task_id
        self.url = None
        self.data = None

    def get_url(self):
        if not self.url:
            self.url = self.api._getTaskById(self.task_id)
        return self.url

    def get_data(self):
        if not self.data and self.get_url():
            self.data = requests.get(self.url).content
        return self.data

class PixaiAPI:
    def __init__(self, token):
        self.base_url = "https://api.pixai.art/graphql"
        self.headers = {
            'User-Agent': "webstar/5.0",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/json"
        }

    def send_request(self, payload):
        try:
            resp = requests.post(self.base_url, json=payload, headers=self.headers)
            return resp.json() if resp.ok else self._handle_error(resp)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def txt2img(self, prompts="1girl", steps=20, modelId=1647780283914444571, samplingMethod="DPM++ 2M Karras", cfgScale=6, size=(512, 512), priority=1000, batchSize=1, lora=None):
        width, height = size
        return PixaiTask(self, self._createGenerationTask(prompts, steps, modelId, samplingMethod, cfgScale, width, height, priority, batchSize, lora))

    def img2img(self, filename, prompts="1girl", steps=20, modelId=1647780283914444571, samplingMethod="DPM++ 2M Karras", cfgScale=6, size=(512, 512), priority=1000, strength=0.65, batchSize=1, lora=None):
        mediaId = self.upload(filename)
        width, height = size
        return PixaiTask(self, self._createGenerationTask(prompts, steps, modelId, samplingMethod, cfgScale, width, height, priority, batchSize, lora, mediaId, strength))

    def _createGenerationTask(self, prompts, steps, modelId, samplingMethod, cfgScale, width, height, priority, batchSize, lora, mediaId=None, strength=None):
        payload = json.loads(CreateGenerationTask)
        parameters = payload['variables']['parameters']

        parameters['prompts'] = prompts
        parameters['samplingSteps'] = steps
        parameters['modelId'] = str(modelId)
        parameters['samplingMethod'] = samplingMethod
        parameters['cfgScale'] = cfgScale
        parameters['width'] = width
        parameters['height'] = height
        parameters['priority'] = priority
        parameters['batchSize'] = batchSize
        if lora:
            parameters['lora'] = lora
        if mediaId:
            parameters['mediaId'] = mediaId
            parameters['strength'] = strength

        response = self.send_request(payload)

        if "error" in response:
            print(f"Failed to create task due to error: {response['error'].get('message')}")
        else:
            task_id = response.get('data', {}).get('createGenerationTask', {}).get('id', None)
            print(f"Task ID: {task_id}" if task_id else "Failed to create task or get a response")
        return task_id

    def _getTaskById(self, task_id):
        payload = json.loads(GetTaskById)
        payload['variables']['id'] = task_id
        response = self.send_request(payload)

        media = response.get('data', {}).get('task', {})['media']
        if media:
            urls = media.get('urls', [])
            return next((url_info['url'] for url_info in urls if url_info.get('variant') == "PUBLIC"), None)

    def upload(self, filename):
        if filename == None:
            return
        uploadMedia = self._uploadMedia()
        uploadUrl = uploadMedia.get('uploadUrl', None)
        externalId = uploadMedia.get('externalId', None)
        if uploadUrl and externalId:
            with open(filename, 'rb') as file:
                requests.put(uploadUrl, data=file.read(), headers={'Content-Type': "image/png"})
            return self._uploadMedia(externalId).get('mediaId', None)

    def _uploadMedia(self, externalId=None):
        payload = json.loads(UploadMedia)
        if externalId:
            payload['variables']['input']["externalId"] = externalId

        response = self.send_request(payload)
        return response.get('data', {}).get('uploadMedia', {})

    @staticmethod
    def _handle_error(response):
        print(f"Error: {response.status_code}, {response.text}")
        return None

