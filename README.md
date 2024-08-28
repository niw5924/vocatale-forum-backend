"""
FastAPI 서버 API 함수들

이 모듈은 게시물과 댓글을 처리하는 API 요청 함수들을 포함하고 있습니다.
각 함수는 비동기로 서버에 요청을 보내고 데이터를 가져오거나 수정, 삭제합니다.

1. get_posts: 모든 게시물을 최신순으로 가져옵니다.
   - 사용법: posts = await get_posts()
   - 실패 시 500 오류를 반환합니다.

2. get_post: 특정 게시물을 ID로 가져옵니다.
   - 사용법: post = await get_post(postId)
   - 실패 시 404 오류("Post not found")를 반환합니다.

3. add_post: 새로운 게시물을 추가합니다.
   - 사용법: new_post = await add_post({"title": "Title", "content": "Content"})
   - 실패 시 500 오류를 반환합니다.

4. edit_post: 기존 게시물을 수정합니다.
   - 사용법: updated_post = await edit_post(postId, {"title": "Updated Title", "content": "Updated Content"})
   - 실패 시 404 오류("Post not found") 또는 500 오류를 반환합니다.

5. delete_post: 게시물을 삭제합니다.
   - 사용법: result = await delete_post(postId)
   - 성공 시 {"message": "Post deleted successfully"}를 반환합니다.
   - 실패 시 404 오류("Post not found") 또는 500 오류를 반환합니다.

6. increase_views: 특정 게시물의 조회수를 증가시킵니다.
   - 사용법: updated_post = await increase_views(postId)
   - 실패 시 404 오류("Post not found") 또는 500 오류를 반환합니다.

7. add_comment: 게시물에 댓글을 추가합니다.
   - 사용법: new_comment = await add_comment(postId, {"content": "Nice post!"})
   - 실패 시 404 오류("Post not found") 또는 500 오류를 반환합니다.

8. delete_comment: 게시물의 특정 댓글을 삭제합니다.
   - 사용법: result = await delete_comment(postId, commentId)
   - 성공 시 {"message": "Comment deleted successfully"}를 반환합니다.
   - 실패 시 404 오류("Comment not found") 또는 500 오류를 반환합니다.
"""
