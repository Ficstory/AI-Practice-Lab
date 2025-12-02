from django.shortcuts import render, redirect, get_object_or_404
from .crawler import fetch_toss_comments
from .models import Comment

# 'index' 뷰는 검색어 처리 및 리다이렉트만 담당 (기존과 동일)
def index(request):
    company_name = request.GET.get('company_name')

    if company_name:
        # 검색 시, 해당 회사의 기존 댓글은 모두 삭제하고 새로 크롤링
        Comment.objects.filter(company_name=company_name).delete()
        
        crawled_data = fetch_toss_comments(company_name)
        stock_code = crawled_data.get('stock_code')
        comments_list = crawled_data.get('comments', [])

        for content in comments_list:
            Comment.objects.create(
                company_name=company_name,
                stock_code=stock_code,
                content=content
            )
        
        # 처리가 끝나면 'index_result'라는 이름의 URL로 이동시킴
        return redirect('crawlings:index_result', company_name=company_name)

    # 검색어가 없으면 그냥 빈 검색 페이지만 보여줌
    return render(request, 'crawlings/index.html')

# 'index_result' 뷰는 결과 페이지만 담당 (기존과 동일)
def index_result(request, company_name):
    # URL로부터 받은 company_name으로 DB에서 댓글 조회
    comments = Comment.objects.filter(company_name=company_name).order_by('-saved_date')
    
    stock_code = None
    if comments.exists():
        # 첫 번째 댓글에서 stock_code를 가져옵니다.
        stock_code = comments.first().stock_code
        
    context = {
        'company_name': company_name,
        'comments': comments,
        'stock_code': stock_code,
    }
    
    return render(request, 'crawlings/index.html', context)

# --- 아래 함수가 새로 추가되었습니다 ---
def delete_comment(request, comment_id):
    """
    주어진 comment_id에 해당하는 댓글을 삭제하고,
    해당 댓글이 속해 있던 회사의 결과 페이지로 리디렉션합니다.
    """
    # 1. 삭제할 댓글 객체를 데이터베이스에서 찾습니다.
    #    만약 해당 ID의 댓글이 없으면 404 에러 페이지를 보여줍니다.
    comment_to_delete = get_object_or_404(Comment, pk=comment_id)
    
    # 2. 삭제 후 리디렉션할 회사의 이름을 변수에 저장해 둡니다.
    #    (객체를 삭제하기 전에 이름을 가져와야 합니다.)
    company_name_for_redirect = comment_to_delete.company_name

    # 3. POST 요청일 경우에만 삭제를 진행합니다. (보안상 권장)
    if request.method == 'POST':
        # 4. 데이터베이스에서 해당 댓글 객체를 삭제합니다.
        comment_to_delete.delete()
        
        # 5. 저장해 둔 회사 이름으로 결과 페이지 URL을 만들어 리디렉션합니다.
        return redirect('crawlings:index_result', company_name=company_name_for_redirect)
    
    # POST 요청이 아니라면(예: 주소창에 URL을 직접 입력), 그냥 검색 결과 페이지로 보냅니다.
    return redirect('crawlings:index_result', company_name=company_name_for_redirect)

