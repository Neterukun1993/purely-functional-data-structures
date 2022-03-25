# purely-functional-data-structures
Purely Functional (Persistent) Data Structures in Python

### basic
- [リスト (List stack)](/src/basic/list_stack.py)
- [停止計算 (Suspension)](/src/basic/suspension.py)
- [ストリーム (Stream)](/src/basic/stream.py)

### queue
- [キュー (Batched queue)](/src/queue/batched_queue.py)
- [銀行家のキュー (Banker's queue)](/src/queue/bankers_queue.py)
- [物理学者のキュー (Physicist's queue)](/src/queue/physicists_queue.py)
- [実時間キュー (Real time queue)](/src/queue/real_time_queue.py)
- [全域再構築キュー (Hood Melville queue)](/src/queue/hood_melville_queue.py)
- [Bootstrapped queue](/src/queue/bootstrapped_queue.py)
- [実時間キューを用いた Bootstrapped queue](/src/queue/bootstrapped_queue_with_real_time_queue.py)
- [暗黙的再帰減速に基づくキュー (Implicit queue)](/src/queue/implicit_queue.py)

### deque
- [両端キュー (Batched Deque)](/src/deque/batched_deque.py)
- [銀行家の両端キュー (Banker's Deque)](/src/deque/bankers_deque.py)
- [実時間両端キュー (Real time Deque)](/src/deque/real_time_deque.py)

### set
- [二分探索木 (Unbalanced tree)](/src/set/unbalanced_set.py)
- [赤黒木 (Red black tree)](/src/set/red_black_set.py)

### finite map
- [二分探索木 (Unbalanced tree)](/src/finite_map/unbalanced_map.py)
- [パトリシア木 (Patricia tree)](/src/finite_map/intmap_patricia_tree.py)

### heap
- [左偏ヒープ (Leftist heap)](/src/heap/leftist_heap.py)
- [スプレーヒープ (Splay heap)](/src/heap/splay_heap.py)
- [ペアリングヒープ (Pairing heap)](/src/heap/pairing_heap.py)
- [二項ヒープ (Binomial heap)](/src/heap/binomial_heap.py)
- [遅延ペアリングヒープ (Lazy pairing heap)](/src/heap/lazy_pairing_heap.py)
- 遅延二項ヒープ
- スケジュール化された二項ヒープ
- ねじれ二項ヒープ


### random access list
- 二進ランダムアクセスリスト
- [ねじれ二進ランダムアクセスリスト (Skew binary random access list)](/src/random_access_list/skew_binary_random_access_list.py)

### catenable list
- [結合可能リスト (Catenable list)](/src/catenable_list/catenable_list.py)
- 結合可能両端キュー

### sortable
- [ボトムアップマージソート (Bottom up merge sort)](/src/sortable/bottom_up_merge_sort.py)
- スケジュール化されたボトムアップマージソート
