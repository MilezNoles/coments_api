from .models import Comment


def path_to_children(id):
    """
    funk to get raw sql to get
    all children from node(id)
    """
    if isinstance(id, tuple):
        where = " in "
    else:
        where = "="
    query = f'''
    WITH RECURSIVE children AS (
        SELECT bcc.*, 0 AS relative_depth,
               array[bcc.id] as path
        FROM blog_comments_comment bcc
        WHERE id{where}%s    
        UNION ALL    
        SELECT bcc.*, c.relative_depth + 1,
               path || bcc.id
        FROM children c JOIN
             blog_comments_comment bcc
             ON bcc.reply_to_id = c.id
                                )
    SELECT id,post_id, name,body, reply_to_id, relative_depth,path, array_length(path, 1) as path_len
    FROM children
    ORDER BY path;
    '''
    return Comment.objects.raw(query, [id])
