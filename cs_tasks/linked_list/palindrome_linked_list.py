# Definition for singly-linked list.

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        is_palindrome = False
        prev_p = head
        curr_p = prev_p.next if prev_p else None
        while curr_p:
            prev_p = curr_p
            curr_p = curr_p.next
        tail = prev_p

        return is_palindrome


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
    print(Solution().isPalindrome(head))


if __name__ == '__main__':
    main()
