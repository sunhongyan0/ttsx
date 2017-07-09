
class sessionMiddleware(object):

    def process_request(self,request):
        path = request.path
        print(path)
        if path not in ['/ttsx/login/','/ttsx/login_handle/','/ttsx/out/',
                        '/ttsx/register/','/ttsx/register_handle/',
                        '/ttsx/register_vaild/']:
            request.session['Path'] = request.get_full_path()
            print(request.get_full_path())

