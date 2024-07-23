UploadMedia = r"""
{
  "query": "mutation uploadMedia($input: UploadMediaInput!) { uploadMedia(input: $input) { uploadUrl externalId mediaId media { ...MediaBase } }} fragment MediaBase on Media { id type width height urls { variant url } imageType fileUrl duration thumbnailUrl hlsUrl size flag { ...ModerationFlagBase }} fragment ModerationFlagBase on ModerationFlag { status isSensitive isMinors isRealistic shouldBlur isWarned}",
  "variables": {
    "input": {
      "provider": "S3",
      "type": "IMAGE"
    }
  }
}
"""

CreateGenerationTask = r"""
{
  "query": "mutation createGenerationTask($parameters: JSONObject!) {createGenerationTask(parameters: $parameters) {    ...TaskBase}} fragment TaskBase on Task {id  userId  parameters  outputs  artworkId  artworkIds  artworks {createdAt  hidePrompts  id  isNsfw  isSensitive  mediaId  title  updatedAt  flag {      ...ModerationFlagBase}}  status\n  priority  runnerId\n  startedAt\n  endAt createdAt  updatedAt  favoritedAt  media {...MediaBase} type {type model} retryCount}fragment ModerationFlagBase on ModerationFlag {  status  isSensitive  isMinors  isRealistic  shouldBlur  isWarned  isAppealable} fragment MediaBase on Media {  id type  width  height  urls {variant url} imageType  fileUrl  duration  thumbnailUrl  hlsUrl  size  flag {...ModerationFlagBase}}",
  "variables": {
    "parameters": {
      "extra": {},
      "negativePrompts": "worst quality, large head, low quality, extra digits, bad eye,  EasyNegativeV2,  ng_deepnegative_v1_75t",
      "autoPublish": false,
      "clipSkip": 2,
      "controlNets": []
    }
  }
}
"""

GetTaskById = r"""
{"query": " query getTaskById($id: ID!) {task(id: $id) {...TaskBase}}fragment TaskBase on Task {id artworks {mediaId}media {...MediaBase}}fragment MediaBase on Media {urls {variant url}}",
  "variables": {
    "id": ""
  }
}
"""

