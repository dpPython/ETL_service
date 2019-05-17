from Contracts.service_api.resource.api_v1 import app, registration

#app.add_task(registration)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8007)
