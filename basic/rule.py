def set_max(x, x_max):
    modify_x = [min(x[i], x_max) for i in range(len(x))]
    return modify_x


def set_min(x, x_min):
    modify_x = [max(x[i], x_min) for i in range(len(x))]
    return modify_x


def set_val(x, val):
    modify_x = [val for i in range(len(x))]
    return modify_x


def modify(artist_id, x):
    # if artist_id == "b15e8846dc61824c1242a6b36796117b":  # 6181
    #     return set_val(x, 6081)
    # ------------------------
    if artist_id == "cd5ce8f47e50971ddb629d86a0bc34f2":
          return set_val(x,6800)

    if artist_id == "c7425ea3ecbea3a51b5550c698be7e71":
         return set_val(x, 200)
    if artist_id == "ca3e42dfdb7529d540141548674bc63e":
         return set_val(x,410)
    if artist_id == "b7522cc91cf57ada15de2298bfd6a3ee":
         return set_val(x,400)
    return x
