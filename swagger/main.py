import os
from logging import getLogger
from string import Template

os.environ["ENV"] = "dev"
application_name = "Snail App Swagger UI"
env_name = os.environ["ENV"]

logger = getLogger(__name__)


def lambda_handler(event, context):
    with open("snail-dev-oas30.json") as f:
        swagger_doc = f.read()
        logger.info("Read file")

    body = generate_swagger_page_body(swagger_doc, application_name)
    return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": body}


def generate_swagger_page_body(swagger_doc, app_name):
    # dict = {}
    # with open(f"swagger/{env_name}vars.ini") as f:
    #     for line in f:
    #         (key, val) = line.split("=")
    #         dict[key] = val.replace("\n", "")
    # template = Template(swagger_doc)
    # swagger_spec = template.safe_substitute(**dict)
    # hide_option = """
    # <style>
    #     .opblock-tag[data-tag='CORS'] {
    #         display: none;
    #     }
    #     div.opblock-options {
    #         display: none;
    #     }
    # </style>
    # """
    # return f"""
    #     <!DOCTYPE html><html lang="en"><head>
    #     <meta charset="UTF-8">
    #     <title>{app_name}</title>
    #     <link rel="stylesheet" href="">
    #     """

    return """
    <html>
  <head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/swagger-ui.css" >
    <style>
      .topbar {
        display: none;
      }
    </style>
  </head>

  <body>
    <div id="swagger-ui"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/swagger-ui-bundle.js"> </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/swagger-ui-standalone-preset.js"> </script>
    <script src="./openapi.js"> </script>
    <script>
      window.onload = function() {
        const ui = SwaggerUIBundle({
          spec: %(spec)s,
          dom_id: '#swagger-ui',
          deepLinking: true,
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset
          ],
          plugins: [
            SwaggerUIBundle.plugins.DownloadUrl
          ],
          layout: "StandaloneLayout"
        })

        window.ui = ui
      }
  </script>
  </body>
</html>""" % {
        "spec": swagger_doc
    }
