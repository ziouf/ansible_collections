
import sys
from ansible.utils.collection_loader import AnsibleCollectionLoader
sys.meta_path.insert(0, AnsibleCollectionLoader())
