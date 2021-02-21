# Definition for singly-linked list.

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def oddEvenList(self, head: ListNode) -> ListNode:
        # print('!!!!!!!!!!!!!!!!!!!')
        odd_head_p = head
        odd_tail_p = odd_head_p
        even_head_p = head.next if head else None
        even_tail_p = even_head_p
        # Input: 1->2->3->4->5->NULL
        # Output: 1->3->5->2->4->NULL
        curr_p = even_tail_p.next if even_tail_p else None
        is_odd = True
        while curr_p:
            # print('---------------------------------')
            # print(curr_p.val if curr_p else None)
            if is_odd:
                odd_tail_p.next = curr_p
                odd_tail_p = odd_tail_p.next
                is_odd = False
            else:  # is_even
                even_tail_p.next = curr_p
                even_tail_p = even_tail_p.next
                is_odd = True
            curr_p = curr_p.next

            # print_list(odd_head_p)
            # print_list(even_head_p)
            # print('---------------------------------')
        if even_tail_p:
            even_tail_p.next = None
        if odd_tail_p:
            odd_tail_p.next = None

        # print('!!!!!!!!!!!!!!!!!!!!!!!')
        # print_list(odd_head_p)
        # print_list(even_head_p)
        # print('---------------------------------')
        if odd_tail_p:
            odd_tail_p.next = even_head_p
        return odd_head_p


def print_list(head: ListNode):
    tail = head
    v = []
    while tail:
        v.append(tail.val)
        tail = tail.next
    print(v)


def main():
    values = [1, 2, 3, 4, 5]
    values = [2, 1, 3, 5, 6, 4, 7]
    head = ListNode(values[0])
    tail = head
    for i in range(1, len(values)):
        point = ListNode(values[i])
        tail.next = point
        tail = point
    print_list(head)
    print_list(Solution().oddEvenList(head))


if __name__ == '__main__':
    main()
