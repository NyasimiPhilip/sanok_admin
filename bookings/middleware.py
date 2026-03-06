from django.utils import timezone
from django.http import HttpResponseForbidden
from django.shortcuts import render


class TechnicianAccessTimeMiddleware:
    """
    Middleware to restrict technician access to morning hours (5 AM - 12 PM)
    Admins can assign orders at any time but technicians can only see them in the morning
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user is authenticated and is a technician
        if request.user.is_authenticated:
            if hasattr(request.user, 'role') and request.user.role == 'technician':
                current_time = timezone.now()
                current_hour = current_time.hour
                
                # Check if it's within morning hours (5 AM to 12 PM)
                if not (5 <= current_hour < 12):
                    # Allow access to logout and static files
                    if not (request.path.startswith('/admin/logout/') or 
                           request.path.startswith('/static/') or
                           request.path.startswith('/media/')):
                        return HttpResponseForbidden(
                            f'''
                            <html>
                            <head>
                                <title>Access Restricted - Morning Hours Only</title>
                                <style>
                                    body {{
                                        font-family: Arial, sans-serif;
                                        display: flex;
                                        justify-content: center;
                                        align-items: center;
                                        height: 100vh;
                                        margin: 0;
                                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    }}
                                    .container {{
                                        background: white;
                                        padding: 40px;
                                        border-radius: 10px;
                                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                                        text-align: center;
                                        max-width: 500px;
                                    }}
                                    h1 {{
                                        color: #dc3545;
                                        margin-bottom: 20px;
                                    }}
                                    p {{
                                        color: #666;
                                        line-height: 1.6;
                                        margin-bottom: 10px;
                                    }}
                                    .time {{
                                        font-size: 24px;
                                        font-weight: bold;
                                        color: #667eea;
                                        margin: 20px 0;
                                    }}
                                    .info {{
                                        background: #f8f9fa;
                                        padding: 20px;
                                        border-radius: 5px;
                                        margin-top: 20px;
                                    }}
                                    .morning {{
                                        color: #28a745;
                                        font-weight: bold;
                                        font-size: 18px;
                                    }}
                                </style>
                            </head>
                            <body>
                                <div class="container">
                                    <h1>🌅 Morning Access Only</h1>
                                    <div class="time">Current Time: {current_time.strftime('%I:%M %p')}</div>
                                    <p>Technician access is only available during <span class="morning">morning hours</span>:</p>
                                    <p><strong>5:00 AM - 12:00 PM (Noon)</strong></p>
                                    <div class="info">
                                        <p>Orders are assigned by admin throughout the day,</p>
                                        <p>but you can view them in the morning shift.</p>
                                        <p><br>Please log in during the morning hours to view your assigned orders.</p>
                                        <p>For urgent matters, contact your administrator.</p>
                                    </div>
                                </div>
                            </body>
                            </html>
                            '''
                        )
        
        response = self.get_response(request)
        return response
